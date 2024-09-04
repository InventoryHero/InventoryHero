from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from backend.db.models.StorageContainer import ContainerTypes, Storage
from backend.decorators import auth, emit_update


def get_storage_helper(storage_type, household, storage_id=None):
    if storage_type not in ContainerTypes:
        return {"status": "storage_type_invalid"}, 400

    storage_container = Storage.query

    if storage_type != ContainerTypes.All:
        storage_container = storage_container.filter_by(type=storage_type)

    storage_container = storage_container.filter_by(household_id=household)

    if storage_id is not None:
        storage_container = storage_container.filter_by(id=storage_id)

    storage_container = storage_container.all()
    return storage_container, 200


class StorageEndpoint(Blueprint):
    def __init__(self, name, import_name, application, db, url_prefix="", *args):
        self.app = application
        self.db = db

        url_prefix += ("" if url_prefix.endswith("/") else "/") + "storage"

        super(StorageEndpoint, self).__init__(name=name, import_name=import_name, url_prefix=url_prefix, *args)

        @self.route("/all", methods=["GET"])
        @jwt_required()
        @auth
        def get_all(household):
            storage_container, code = get_storage_helper(ContainerTypes.All, household)
            return jsonify(storage_container), code

        @self.route("/box/<int:box_id>", methods=["GET"])
        @self.route("/box", defaults={'box_id': None}, methods=["GET"])
        @jwt_required()
        @auth
        def get_boxes(household, box_id):
            self.app.logger.info(box_id)
            result, code = get_storage_helper(ContainerTypes.Box, household, box_id)
            self.app.logger.info(code)
            self.app.logger.warn(result)
            if code != 200:
                return result, code

            get_contained_amount = request.args.get('contained', None)
            self.app.logger.info("get contained amount")
            storage_container = []
            for container in result:
                serialized = container.serialize()
                if get_contained_amount is not None:
                    serialized["products"] = len(container.product_mappings)
                storage_container.append(serialized)

            return jsonify(storage_container), 200

        @self.route("/location/<int:location_id>", methods=["GET"])
        @self.route("/location", defaults={'location_id': None} ,methods=["GET"])
        @jwt_required()
        @auth
        def get_locations(household, location_id):
            result, code = get_storage_helper(ContainerTypes.Location, household, location_id)
            if code != 200:
                return result, code
            get_contained_amount = request.args.get('contained', None)
            storage_container = []
            for container in result:
                serialized = container.serialize()

                if get_contained_amount is not None:
                    serialized["products"] = len(container.product_mappings)
                    serialized["boxes"] = len(container.children)

                storage_container.append(serialized)

            return jsonify(storage_container), 200

        @self.route("/box/content/<int:id>", methods=["GET"])
        @jwt_required()
        @auth
        def get_content(household, id):
            storage = Storage.query.filter_by(
                household_id=household,
                id=id,
                type=ContainerTypes.Box
            ).first()
            if storage is None:
                return jsonify(status="box_not_found"), 400
            content = {
                "products": storage.serialize_content()
            }
            return jsonify(content=content), 200

        @self.route("/location/content/<int:id>", methods=["GET"])
        @jwt_required()
        @auth
        def get_location_content(household, id):
            storage = Storage.query.filter_by(
                household_id=household,
                id=id,
                type=ContainerTypes.Location
            ).first()
            if storage is None:
                return {"status": "location_not_found"}, 400
            content = {
                "content": storage.serialize_content()
            }
            self.app.logger.info(content)
            return jsonify(content), 200

        @self.route("/box/add", methods=["POST"])
        @jwt_required()
        @auth
        @emit_update()
        def add_box(household):
            storage_name = request.json.pop("name", "")
            if storage_name == "":
                return jsonify(status="create_box_invalid_name"), 400

            location = request.json.pop("location_id", None)
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
        @auth
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
        @auth
        @emit_update()
        def delete_box(household, box_id):
            box = Storage.query.filter_by(
                id=box_id,
                household_id=household,
                type=ContainerTypes.Box
            ).first()
            if box is None:
                return jsonify(status="box_not_found"), 204

            self.db.session.delete(box)
            self.db.session.commit()
            return {}, 204

        @self.route("/box/<int:box_id>", methods=["POST"])
        @jwt_required()
        @auth
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
            new_location = to_update.get("location_id", None)

            if new_name != box.name:
                box.name = new_name

            # TODO CHECK IF THIS NEW ID EXISTS
            if new_location != box.storage_id:
                box.storage_id = new_location

            self.db.session.commit()
            self.app.logger.warning(box.serialize())
            return jsonify(updated=box.serialize()), 200

        @self.route("/location/<int:location_id>", methods=["DELETE"])
        @jwt_required()
        @auth
        @emit_update()
        def delete_location(household, location_id):
            location = Storage.query.filter_by(
                id=location_id,
                household_id=household,
                type=ContainerTypes.Location
            ).first()
            if location is None:
                return jsonify(status="location_not_found"), 400

            self.db.session.delete(location)
            self.db.session.commit()
            self.app.logger.info(f"DELETED BOX {location.name}")
            return {}, 204

        @self.route("/location/<int:location_id>", methods=["POST"])
        @jwt_required()
        @auth
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

            if new_name != location.name:
                location.name = new_name

            self.db.session.commit()
            self.app.logger.warning(location.serialize())
            return jsonify(updated=location.serialize()), 200

        @self.route("/box/<int:box_id>/name", methods=["GET"])
        @jwt_required()
        @auth
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
        @auth
        def location_name(household, location_id):
            location = Storage.query.filter_by(
                id=location_id,
                household_id=household,
                type=ContainerTypes.Location
            ).first()
            if location is None:
                return jsonify(status="location_not_found"), 400

            return jsonify(name=location.name), 200
