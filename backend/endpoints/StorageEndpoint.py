from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import desc
from sqlalchemy.orm import aliased, contains_eager

from backend.db.models.StorageContainer import ContainerTypes, Storage
from backend.decorators import require_household_member, emit_update
from backend.db.models.Product import Product, ProductContainerMapping



def get_storage_helper(storage_type, household, storage_id=None):
    if storage_type not in ContainerTypes:
        return {"status": "storage_type_invalid"}, 400

    storage_container = Storage.query

    if storage_type != ContainerTypes.All:
        storage_container = storage_container.filter_by(type=storage_type)

    storage_container = storage_container.filter_by(household_id=household)

    if storage_id is not None:
        storage_container = storage_container.filter_by(id=storage_id)

    storage_container = storage_container.order_by(desc(Storage.type)).all()
    return storage_container, 200


class StorageEndpoint(Blueprint):
    def __init__(self, name, import_name, application, db, url_prefix="", *args):
        self.app = application
        self.db = db

        url_prefix += ("" if url_prefix.endswith("/") else "/") + "storage"

        super(StorageEndpoint, self).__init__(name=name, import_name=import_name, url_prefix=url_prefix, *args)

        @self.route("/all", methods=["GET"])
        @jwt_required()
        @require_household_member
        def get_all(household):
            self.app.logger.info("motherfucker")
            storage_container, code = get_storage_helper(ContainerTypes.All, household)
            return jsonify(storage_container), code

        @self.route("/box/<int:box_id>", methods=["GET"])
        @self.route("/box", defaults={'box_id': None}, methods=["GET"])
        @jwt_required()
        @require_household_member
        def get_boxes(household, box_id):
            self.app.logger.info(box_id)
            result, code = get_storage_helper(ContainerTypes.Box, household, box_id)
            self.app.logger.info(code)
            self.app.logger.warn(result)
            if code != 200:
                return result, code
            return jsonify(result), 200

        @self.route("/location/<int:location_id>", methods=["GET"])
        @self.route("/location", defaults={'location_id': None} ,methods=["GET"])
        @jwt_required()
        @require_household_member
        def get_locations(household, location_id):
            result, code = get_storage_helper(ContainerTypes.Location, household, location_id)
            if code != 200:
                return result, code
            self.app.logger.info(result)
            return jsonify(result), 200

        @self.route("/box/content/<int:id>", methods=["GET"])
        @jwt_required()
        @require_household_member
        def get_content(household, id):
            storage = Storage.query.filter_by(
                household_id=household,
                id=id,
                type=ContainerTypes.Box
            ).first()
            if storage is None:
                return jsonify(status="box_not_found"), 400
            filtered_products = (
                self.db.session.query(Product)
                .join(ProductContainerMapping, Product.mappings)
                .filter(ProductContainerMapping.storage_id == storage.id, Product.household_id == household)
                #.options(contains_eager(Product.mappings))
                .all()
            )
            mappings = (
                self.db.session.query(ProductContainerMapping)
                .filter_by(storage_id=storage.id)
                .all()
            )

            self.app.logger.info(filtered_products)
            return jsonify(content={
                "products": filtered_products,
                "storageLocations": mappings
            }), 200

        @self.route("/location/content/<int:id>", methods=["GET"])
        @jwt_required()
        @require_household_member
        def get_location_content(household, id):
            storage = Storage.query.filter_by(
                household_id=household,
                id=id,
                type=ContainerTypes.Location
            ).first()
            if storage is None:
                return {"status": "location_not_found"}, 400
            filtered_products = (
                self.db.session.query(Product)
                .join(ProductContainerMapping, Product.mappings)
                .filter(ProductContainerMapping.storage_id == storage.id, Product.household_id == household)
                #.options(contains_eager(Product.mappings))
                .all()
            )

            mappings = (
                self.db.session.query(ProductContainerMapping)
                .filter_by(storage_id=storage.id)
                .all()
            )

            filtered_boxes = (
                self.db.session.query(Storage)
                .filter(Storage.storage_id == storage.id, Storage.household_id == household)
                .options(contains_eager(Storage.children))  # Eager load the children relationship
                .all()
            )
            return jsonify(content={
                "boxes": filtered_boxes,
                "products": filtered_products,
                "storageLocations": mappings
            }), 200

        @self.route("/box/add", methods=["POST"])
        @jwt_required()
        @require_household_member
        @emit_update()
        def add_box(household):
            storage_name = request.json.pop("name", "")
            if storage_name == "":
                return jsonify(status="create_box_invalid_name"), 400

            location = request.json.pop("storageId", None)
            location_id = None
            if location is not None:
                location = Storage.query.filter_by(household_id=household, id=location).first()
                if location is None:
                    return jsonify(status="create_box_storage_not_found"), 400
                location_id = location.id

            box = Storage.query.filter_by(
                household_id=household,
                name=storage_name,
                type=ContainerTypes.Box
            ).first()
            if box is not None:
                return jsonify(status="create_box_name_exists"), 400

            box = Storage(
                name=storage_name,
                household_id=household,
                storage_id=location_id,
                type=ContainerTypes.Box
            )
            self.db.session.add(box)
            self.db.session.commit()
            new_storage = Storage.query.filter_by(id=box.id).first()
            return jsonify(new_storage), 201

        @self.route("/location/add", methods=["POST"])
        @jwt_required()
        @require_household_member
        @emit_update()
        def add_location(household):
            storage_name = request.json.pop("name", "")
            if storage_name == "":
                return jsonify(status="create_location_invalid_name"), 400

            location = Storage.query.filter_by(
                name=storage_name,
                household_id=household,
                type=ContainerTypes.Location
            ).first()
            if location is not None:
                return jsonify(status="create_location_name_exists"), 409

            location = Storage(
                name=storage_name,
                household_id=household,
                type=ContainerTypes.Location
            )
            self.db.session.add(location)
            self.db.session.commit()
            return jsonify(location), 201

        @self.route("/box/<int:box_id>", methods=["DELETE"])
        @jwt_required()
        @require_household_member
        @emit_update()
        def delete_box(household, box_id):
            box = Storage.query.filter_by(
                id=box_id,
                household_id=household,
                type=ContainerTypes.Box
            ).first()
            if box is None:
                return jsonify(status="box_not_found"), 204
            # TODO JUST DELETING SETS THE IDs to NONE
            # AS EXPECTED FORM DB
            # CHECK BEFORE IF SOME PRODUCTS ALREADY EXIST IN "VOID"
            # TO MERGE PROPERLY
            self.db.session.delete(box)
            self.db.session.commit()
            return {}, 204

        @self.route("/box/<int:box_id>", methods=["POST"])
        @jwt_required()
        @require_household_member
        @emit_update()
        def edit_box(household, box_id):
            box = Storage.query.filter_by(
                id=box_id,
                household_id=household,
                type=ContainerTypes.Box
            ).first()
            if box is None:
                return jsonify(status="box_not_found"), 400

            to_update = request.json.get("storage", None)
            if box is None:
                return jsonify(status="update_box_no_data"), 400

            new_name = to_update.get("name", box.name)
            new_storage = to_update.get("storageId", None)

            if new_name != box.name:
                box.name = new_name

            location = Storage.query.filter_by(
                household_id=household,
                id=new_storage,
                type=ContainerTypes.Location
            ).first()
            if location is None and new_storage is not None:
                new_storage = box.storage_id
            if new_storage != box.storage_id:
                box.storage_id = new_storage

            self.db.session.commit()
            self.app.logger.warning(box)
            box = Storage.query.filter_by(id=box.id).first()
            return jsonify(updated=box), 200

        @self.route("/location/<int:location_id>", methods=["DELETE"])
        @jwt_required()
        @require_household_member
        @emit_update()
        def delete_location(household, location_id):
            location = Storage.query.filter_by(
                id=location_id,
                household_id=household,
                type=ContainerTypes.Location
            ).first()
            if location is None:
                return jsonify(status="location_not_found"), 400
            # TODO JUST DELETING SETS THE IDs to NONE
            # AS EXPECTED FORM DB
            # CHECK BEFORE IF SOME PRODUCTS ALREADY EXIST IN "VOID"
            # TO MERGE PROPERLY
            self.db.session.delete(location)
            self.db.session.commit()
            self.app.logger.info(f"DELETED BOX {location.name}")
            return {}, 204

        @self.route("/location/<int:location_id>", methods=["POST"])
        @jwt_required()
        @require_household_member
        @emit_update()
        def edit_location(household, location_id):
            location = Storage.query.filter_by(
                id=location_id,
                household_id=household,
                type=ContainerTypes.Location
            ).first()
            if location is None:
                return jsonify(status="location_not_found"), 400

            to_update = request.json.get("storage", None)
            if location is None:
                return jsonify(status="location_no_update_data"), 400

            new_name = to_update.get("name", location.name)

            if new_name == "":
                return jsonify(status="invalid_update_data"), 400

            if new_name != location.name:
                location.name = new_name

            self.db.session.commit()
            return jsonify(updated=location), 200

        @self.route("/box/<int:box_id>/name", methods=["GET"])
        @jwt_required()
        @require_household_member
        def box_name(household, box_id):
            box = Storage.query.filter_by(
                id=box_id,
                household_id=household,
                type=ContainerTypes.Box
            ).first()
            if box is None:
                return jsonify(status="box_not_found"), 400

            return jsonify(name=box.name), 200

        @self.route("/location/<int:location_id>/name", methods=["GET"])
        @jwt_required()
        @require_household_member
        def location_name(household, location_id):
            location = Storage.query.filter_by(
                id=location_id,
                household_id=household,
                type=ContainerTypes.Location
            ).first()
            if location is None:
                return jsonify(status="location_not_found"), 400

            return jsonify(name=location.name), 200

