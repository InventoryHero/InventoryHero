from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from backend.db.models.StorageContainer import Location, Box, ContainerTypes
from backend.decorators import auth, emit_update


def get_storage_helper(storage_type, household, storage_id=None):
    if storage_type == ContainerTypes.Box:
        storage_container = Box.query
        if storage_container is None:
            return {"status": "box_not_found"}, 400
    elif storage_type == ContainerTypes.Location:
        storage_container = Location.query
        if storage_container is None:
            return {"status": "location_not_found"}, 400
    else:
        return {"status": "storage_type_invalid"}, 400

    storage_container = storage_container.filter_by(household_id=household)
    if storage_id is not None:
        storage_container = storage_container.filter_by(id=storage_id)
    if storage_container is None:
        return jsonify(status="no_storage_given"), 400
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
            boxes, code = get_storage_helper(ContainerTypes.Box, household)
            if code != 200:
                return boxes, code
            locations, code = get_storage_helper(ContainerTypes.Location, household)
            if code != 200:
                return locations, code

            storage_container = [container.serialize() for container in boxes + locations]
            return jsonify(storage_container), 200

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
            self.app.logger.info(f"get contained amount {get_contained_amount} hello" )
            storage_container = []
            for container in result:
                serialized = container.serialize()

                if get_contained_amount is not None:
                    self.app.logger.info(container.boxes)
                    serialized["products"] = len(container.product_mappings)
                    serialized["boxes"] = len(container.boxes)

                storage_container.append(serialized)

            return jsonify(storage_container), 200

        @self.route("/box/content/<int:id>", methods=["GET"])
        @jwt_required()
        @auth
        def get_content(household, id):
            storage = Box.query.filter_by(household_id=household, id=id).first()
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
            storage = Location.query.filter_by(household_id=household, id=id).first()
            if storage is None:
                return {"status": "location_not_found"}, 400
            content = {
                "content": storage.serialize_content()
            }
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
                location = Location.query.filter_by(household_id=household, id=location).first()
                if location is None:
                    return jsonify(status="create_box_storage_not_found"), 400
                location_id = location.id

            unique = Box.query.filter_by(household_id=household, name=storage_name).first() is None
            if not unique:
                return jsonify(status="create_box_name_exists"), 400

            new_box = Box(name=storage_name, household_id=household, location_id=location_id)
            self.db.session.add(new_box)
            self.db.session.commit()
            new_storage = Box.query.filter_by(id=new_box.id).first()
            return jsonify(new_storage), 201

        @self.route("/location/add", methods=["POST"])
        @jwt_required()
        @auth
        @emit_update()
        def add_location(household):
            location_name = request.json.pop("name", "")
            if location_name == "":
                return jsonify(status="create_location_invalid_name"), 400

            location = Location.query.filter_by(name=location_name, household_id=household).first()
            if location is not None:
                return jsonify(status="create_location_name_exists"), 409

            new_location = Location(name=location_name, household_id=household)
            self.db.session.add(new_location)
            self.db.session.commit()
            return jsonify(new_location), 201

        @self.route("/box/<int:box_id>", methods=["DELETE"])
        @jwt_required()
        @auth
        @emit_update()
        def delete_box(household, box_id):
            box = Box.query.filter_by(id=box_id, household_id=household).first()
            if box is None:
                return jsonify(status="box_not_found"), 204
            for product in box.product_mappings:
                product.storage_id = None
                product.storage_type = int(ContainerTypes.NoContainer)

            self.db.session.delete(box)
            self.db.session.commit()
            self.app.logger.info(f"DELETED BOX {box.name}")
            return {}, 204

        @self.route("/box/<int:box_id>", methods=["POST"])
        @jwt_required()
        @auth
        @emit_update()
        def edit_box(household, box_id):
            box = Box.query.filter_by(id=box_id, household_id=household).first()
            if box is None:
                return jsonify(status="box_not_found"), 400

            to_update = request.json.get("storage", None)
            if box is None:
                return jsonify(status="update_box_no_data"), 400

            new_name = to_update.get("name", box.name)
            new_location = to_update.get("location_id", None)

            if new_name != box.name:
                box.name = new_name
            if new_location != box.location_id:
                box.location_id = new_location

            self.db.session.commit()
            self.app.logger.warning(box.serialize())
            return jsonify(updated=box.serialize()), 200

        @self.route("/location/<int:location_id>", methods=["DELETE"])
        @jwt_required()
        @auth
        @emit_update()
        def delete_location(household, location_id):
            location = Location.query.filter_by(id=location_id, household_id=household).first()
            if location is None:
                return jsonify(status="location_not_found"), 400

            for product in location.product_mappings:
                product.storage_id = None
                product.storage_type = int(ContainerTypes.NoContainer)
            for box in location.boxes:
                box.storage_id = None

            self.db.session.delete(location)
            self.db.session.commit()
            self.app.logger.info(f"DELETED BOX {location.name}")
            return {}, 204

        @self.route("/location/<int:location_id>", methods=["POST"])
        @jwt_required()
        @auth
        @emit_update()
        def edit_location(household, location_id):
            location = Location.query.filter_by(id=location_id, household_id=household).first()
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
            box = Box.query.filter_by(id=box_id, household_id=household).first()
            if box is None:
                return jsonify(status="box_not_found"), 400

            return jsonify(name=box.name), 200

        @self.route("/location/<int:location_id>/name", methods=["GET"])
        @jwt_required()
        @auth
        def location_name(household, location_id):
            location = Location.query.filter_by(id=location_id, household_id=household).first()
            if location is None:
                return jsonify(status="location_not_found"), 400

            return jsonify(name=location.name), 200
