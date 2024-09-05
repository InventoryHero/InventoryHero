import datetime
import json

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from werkzeug.datastructures import auth

from backend.flask_config import socketio
from backend.db.models.Product import Product, ProductContainerMapping
from backend.db.models.StorageContainer import Storage, ContainerTypes
from backend.decorators import auth, emit_update
from typing import Optional


def get_storage(storage_type, storage, household):
    if storage_type == ContainerTypes.All:
        return None, None

    result = Storage.query.filter_by(
        id=storage,
        household_id=household,
        type=storage_type
    ).first()
    if result is None:
        return None, None
    return result, result.id


# TODO errors
def parse_storage_params(id, type, household):
    try:
        storage_type = ContainerTypes(int(type))
    except ValueError:
        return False, {"status": "storage_type_invalid"}, 400

    if storage_type == ContainerTypes.NoContainer:
        return True, {"id": None, "type": ContainerTypes.NoContainer}, 200

    storage, _ = get_storage(storage_type, id, household)

    if storage is None:
        return False, {"status": "storage_not_found"}, 400

    return True, {"id": storage.id, "type": storage_type}, 200


def check_storage_for_update(storage, entry, household, all_entries):

    storage_id = None
    storage_type = None
    if storage is not None:
        storage = Storage.query.filter_by(
            id=storage,
            household_id=household
        ).first()

        if storage is None:
            return {
                "error": (jsonify(status="storage_not_found"), 400)
            }

        storage_id = storage.id
        storage_type = storage.type

    curr_storage = entry.storage_id

    if storage_id == curr_storage:
        return {}
    for entry in all_entries:
        if entry.storage_id == storage_id:
            return {
                "merge_with": entry,
                "update": True,
            }

    return {
        "update": True,
        "storage_id": storage_id,
        "storage_type": storage_type
    }



class ProductEndpoint(Blueprint):
    def __init__(self, name, import_name, application, db, url_prefix="", *args):
        self.app = application
        self.db = db

        url_prefix += ("" if url_prefix.endswith("/") else "/") + "products"

        super(ProductEndpoint, self).__init__(name=name, import_name=import_name, url_prefix=url_prefix, *args)

        @self.route("/create/<int:product_id>", methods=["POST"])
        @self.route("/create", defaults={'product_id': None}, methods=["POST"])
        @jwt_required()
        @auth
        @emit_update()
        def create_product(household, product_id):
            product_name = request.json.get("name", None)
            if product_name is not None:
                product = Product.query.filter_by(name=product_name, household_id=household).first()
                if product is not None:
                    return jsonify(status="create_product_already_exists"), 400
            elif product_id is not None:
                product = Product.query.filter_by(id=product_id, household_id=household).first()
                if product is None:
                    return jsonify(status="add_product_not_found"), 400
            else:
                return jsonify(status="create_product_invalid_data"), 400

            starred = request.json.get("starred", False)
            creation_date = datetime.datetime.now(datetime.UTC)
            storage_id = request.json.get("storage_id", None)
            storage_type = request.json.get("storage_type", 0)
            storage_valid, ret, code = parse_storage_params(storage_id, storage_type, household)
            if not storage_valid:
                return ret, code
            else:
                storage_type = ret["type"]
                storage_id = ret["id"]

            amount = request.json.get("amount", 0)
            updated_at = creation_date

            added_to_existing = False

            if product_id is not None:
                existing_mapping = ProductContainerMapping.query.filter_by(product_id=product.id, storage_id=storage_id,
                                                                           storage_type=int(storage_type)).first()
                if existing_mapping is not None:
                    existing_mapping.amount += amount
                    added_to_existing = True
            else:
                product = Product(name=product_name, household_id=household, starred=starred,
                                  creation_date=creation_date)
                self.db.session.add(product)
                self.db.session.flush()
            if not added_to_existing:
                production_at_container = ProductContainerMapping(product_id=product.id, amount=amount,
                                                                  storage_id=storage_id, storage_type=int(storage_type),
                                                                  updated_at=updated_at)
                self.db.session.add(production_at_container)

            self.db.session.commit()
            self.app.logger.info(f"Product: {product_name} with amount: {amount} successfully created, "
                                 f"at sttorage: {storage_id} storage_type: {storage_type}")
            self.app.logger.info(household)

            return jsonify(product.serialize()), 200

        @self.route("/<int:product_id>", methods=["GET"])
        @self.route("", defaults={'product_id': None}, methods=["GET"])
        @jwt_required()
        @auth
        def get_products(household, product_id):
            get_starred = request.args.get("starred", None)

            products = Product.query.filter_by(household_id=household)
            if get_starred is not None:
                products = products.filter(Product.starred)
            if product_id is not None:
                products = products.filter_by(id=product_id)

            products = products.all()
            if product_id is None and products is None:
                return {"status": "product_not_found"}, 400

            return jsonify(products), 200

        @self.route("/stored/<int:product_id>", methods=["GET"])
        @jwt_required()
        @auth
        def get_product_stored_at(household, product_id):
            product = Product.query.filter_by(id=product_id, household_id=household).first()

            if product is None:
                return {"status": "product_not_found"}, 400

            return jsonify(product.mappings), 200

        @self.route("/<int:product_id>", methods=["DELETE"])
        @jwt_required()
        @auth
        @emit_update()
        def delete_product(household, product_id):
            product = Product.query.filter_by(id=product_id, household_id=household).first()
            if product_id is None:
                return jsonify(status="product_not_found"), 400

            self.db.session.delete(product)
            self.db.session.commit()
            return {}, 204

        @self.route("/update/<int:product_id>", methods=["POST"])
        @jwt_required()
        @auth
        @emit_update()
        def update_product(household, product_id):
            to_update = request.json.get("product", None)
            if to_update is None:
                return jsonify(status="update_product_no_data"), 400
            product = Product.query.filter_by(id=product_id, household_id=household).first()
            if product is None:
                return jsonify(status="product_not_found"), 400
            new_name = to_update.get('name', None)
            if new_name is None or new_name == '':
                return jsonify(status="update_product_invalid_data"), 400
            product.name = new_name

            self.db.session.commit()
            self.app.logger.info(f"UPDATED PRODUCT {product.name}")
            return jsonify(updated=product), 200

        @self.route("/stored/<int:mapping_id>", methods=["POST"])
        @jwt_required()
        @auth
        @emit_update()
        def update_product_mapping(mapping_id, household):
            new_amount = request.json.get("amount", None)
            storage = request.json.get("storage", None)
            self.app.logger.info(storage)
            mapping = ProductContainerMapping.query.filter_by(id=mapping_id).first()
            product_id = (mapping.product_id if mapping is not None else None)
            product = Product.query.filter_by(id=product_id, household_id=household).first()

            if product is None or mapping is None:
                return jsonify(status="product_not_found_at_storage"), 400

            update = False
            if new_amount is not None:
                if new_amount < 0:
                    return jsonify(status="update_product_at_storage_invalid_data"), 400
                mapping.amount = new_amount
                update = True

            storage_check = check_storage_for_update(storage, mapping, household, product.mappings)

            storage_error = storage_check.get('error', None)
            if storage_error is not None:
                return storage_error

            storage_merge_with: Optional[ProductContainerMapping] = storage_check.get('merge_with', None)
            deleted = None
            if storage_merge_with is not None:
                self.app.logger.info(storage_merge_with)
                self.app.logger.info(mapping)
                update |= True
                mapping.amount += storage_merge_with.amount
                mapping.storage_id = storage_merge_with.storage_id
                deleted = storage_merge_with
                self.db.session.delete(deleted)
            elif storage_check.get('update', False):
                update |= True
                mapping.storage_id = storage_check.get('storage_id', None)
            if update:
                mapping.updated_at = datetime.datetime.now(datetime.UTC)
                self.db.session.commit()
                mapping = ProductContainerMapping.query.filter_by(id=mapping.id).first()
                return jsonify(updated=mapping, deleted=deleted), 200
            return jsonify(), 200

        @self.route("/stored/<int:mapping_id>", methods=["DELETE"])
        @jwt_required()
        @auth
        @emit_update()
        def delete_mapping(mapping_id, household):
            mapping = ProductContainerMapping.query.filter_by(id=mapping_id).first()
            product_id = (mapping.product_id if mapping is not None else None)
            product = Product.query.filter_by(id=product_id, household_id=household).first()
            if product is None or mapping is None:
                return jsonify(status="product_not_found_at_storage"), 400
            self.db.session.delete(mapping)
            self.db.session.commit()
            return {}, 200

