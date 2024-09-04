import uuid

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user

from backend.decorators import auth
from backend.endpoints.Helper import user_in_household
from backend.db.models.User import User as ApplicationUser, Household, HouseholdMembers


class HouseholdEndpoint(Blueprint):
    def __init__(self, name, import_name, application, db, url_prefix, *args):
        self.app = application
        self.db = db

        url_prefix += ("" if url_prefix.endswith("/") else "/") + "household"

        super(HouseholdEndpoint, self).__init__(name=name, import_name=import_name, url_prefix=url_prefix, *args)

        @self.route('/create', methods=["POST"])
        @jwt_required()
        def create_household():
            household_name = request.json.get("name", None)
            if household_name is None:
                return {"status": "invalid_household_name"}, 400

            household = Household.query.filter_by(name=household_name) \
                                    .join(HouseholdMembers).filter_by(member_id=current_user.id).first()

            in_household = user_in_household(current_user.id, household.id if household is not None else None)
            if in_household:
                return {"status": "duplicate_household_name"}, 400
            household = Household(name=household_name, creator=current_user.id)
            self.db.session.add(household)
            self.db.session.commit()

            member = HouseholdMembers(household_id=household.id, member_id=current_user.id, joined=True)
            self.db.session.add(member)
            self.db.session.commit()

            return {}, 200

        @self.route("/all", methods=["GET"])
        @jwt_required()
        def get_households():
            households = HouseholdMembers.query.filter_by(member_id=current_user.id).all()
            if households is None or len(households) == 0:
                return {"status": "no_households"}, 204
            households = [household.household.serialize() for household in households]
            self.app.logger.info(households)
            return jsonify(households), 200

        @self.route("/code/<int:household>", methods=["GET"])
        @jwt_required()
        @auth
        def get_household_invite_code(household):
            # TODO FIND A WAY TO INVALIDATE THOSE AFTER A WHILE (SO NO SPAMMING IS ALLOWED) ...
            household = Household.query.filter_by(id=household, creator=current_user.id).first()
            if household is None:
                return jsonify(status="invite_not_possible"), 403

            invite_code = uuid.uuid4()
            member = HouseholdMembers(household_id=household.id, joined=False, invite=invite_code)
            self.db.session.add(member)
            self.db.session.commit()
            return jsonify(code=str(invite_code)), 200

        @self.route("/meta/<string:invite_code>", methods=["GET"])
        @jwt_required()
        def get_household_invite_meta(invite_code):
            # TODO PROHIBIT OWN HOUSEHOLD JOINING
            invite_code = uuid.UUID(invite_code)
            member = HouseholdMembers.query.filter_by(invite=invite_code).first()
            if member is None:
                return jsonify(status="invite_code_invalid"), 403
            creator = ApplicationUser.query.filter_by(id=member.household.creator).first()
            if creator is None:
                return jsonify(), 500

            if creator.id == current_user.id:
                return jsonify(status="already_member"), 400

            return jsonify(
                owner=creator.username,
                name=member.household.name
            ), 200

        @self.route("/join/<string:invite_code>", methods=["GET"])
        @jwt_required()
        def join_household(invite_code):
            invite_code = uuid.UUID(invite_code)
            member = HouseholdMembers.query.filter_by(invite=invite_code).first()
            if member is None or member.joined:
                return jsonify(status="invite_code_invalid"), 403

            user = HouseholdMembers.query.filter_by(household_id=member.household_id, member_id=current_user.id).first()
            if user is not None and user.id == current_user.id:
                return jsonify(status="already_member"), 400

            member.member_id = current_user.id
            member.invite = None
            member.joined = True
            self.db.session.commit()
            return jsonify(), 200

