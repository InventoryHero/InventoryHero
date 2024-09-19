import uuid

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy.orm import contains_eager

from backend.decorators import require_household_member, household_owner
from backend.endpoints.Helper import user_in_household
from backend.db.models.User import User as ApplicationUser, Household, HouseholdMembers, User
from flask_socketio import emit
from backend.sockets.SidManager import general_socket_sid_mapping


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
            if household_name is None or household_name == "" or len(household_name) > 25:
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

            return jsonify(household=household), 200

        @self.route("/all", methods=["GET"])
        @jwt_required()
        def get_households():
            households = HouseholdMembers.query.filter_by(member_id=current_user.id).all()
            households = (
                self.db.session.query(Household)
                .join(HouseholdMembers, Household.members)
                .filter(HouseholdMembers.member_id == current_user.id)
                .options(contains_eager(Household.members))
                .all()
            )

            if households is None or len(households) == 0:
                return {"status": "no_households"}, 204

            return jsonify(households), 200

        @self.route("/code/<int:household>", methods=["GET"])
        @jwt_required()
        @require_household_member
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
            invite_code = uuid.UUID(invite_code)
            invite = HouseholdMembers.query.filter_by(invite=invite_code).first()
            if invite is None:
                return jsonify(status="invite_code_invalid"), 403
            creator = ApplicationUser.query.filter_by(id=invite.household.creator).first()
            if creator is None:
                return jsonify(), 500

            member = HouseholdMembers.query.filter_by(household_id=invite.household_id,
                                                      member_id=current_user.id).first()
            if member is not None:
                return jsonify(status="already_member"), 400

            return jsonify(
                owner=creator.username,
                name=invite.household.name
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

            return jsonify(household=member.household), 200

        @self.route("/leave/<int:household>", methods=["POST"])
        @jwt_required()
        def leave_household(household):
            member = HouseholdMembers.query.filter_by(household_id=household, member_id=current_user.id).first()
            if member is None:
                return jsonify(status="leave_no_member"), 403
            self.db.session.delete(member)
            self.db.session.commit()
            return jsonify(), 204

        @self.route("/members/<int:household>", methods=["GET"])
        @jwt_required()
        @household_owner()
        def get_members(household):
            members = HouseholdMembers.query.filter_by(household_id=household).all()
            return jsonify(members=members), 200

        @self.route("/<int:household>", methods=["DELETE"])
        @jwt_required()
        @household_owner()
        def delete_household(household):
            household = Household.query.filter_by(id=household).first()
            members = HouseholdMembers.query.filter_by(household_id=household.id).all()

            for member in members:
                if member.user is None:
                    continue
                sid = general_socket_sid_mapping.get(member.user.username)
                if sid is None:
                    continue
                emit("deleted", {
                    "status": "ok",
                    "content": {
                        "household": household.id
                    }
                }, to=sid, namespace='/general')

            self.db.session.delete(household)
            self.db.session.commit()
            return jsonify(), 204

        @self.route("/kick/<int:household>/<int:member_id>", methods=["POST"])
        @jwt_required()
        @household_owner()
        def kick_from_household(household, member_id):
            member = HouseholdMembers.query.filter_by(household_id=household, id=member_id).first()
            if member is None:
                return jsonify(status="member_not_found"), 404
            creator = None
            sid = None
            if member.user is not None:
                creator = Household.query.filter_by(id=household, creator=member.user.id).first()
                sid = general_socket_sid_mapping.get(member.user.username)

            if creator is not None:
                return jsonify(status="cannot_kick_yourself"), 400

            self.db.session.delete(member)
            self.db.session.commit()

            if sid is None:
                return jsonify(), 204

            emit("kicked", {
                "status": "ok",
                "content": {
                    "household": household
                }
            }, to=sid, namespace="/general")

            return jsonify(), 204

        @self.route("/update/<int:household>", methods=["POST"])
        @jwt_required()
        @household_owner()
        def update_household(household):
            household = Household.query.filter_by(id=household).first()
            update_data = request.json.get("household", None)
            if update_data is None:
                return jsonify(status="household_invalid_update_data"), 400
            household_name = update_data.get("name", "")
            if household_name == "" or len(household_name) > 25:
                return jsonify(status="household_invalid_update_data"), 400
            household.name = household_name
            self.db.session.commit()
            return jsonify(household=household), 200

        @self.route("/transfer/<int:household>/<string:username>", methods=["POST"])
        @jwt_required()
        @household_owner()
        def transfer_household(household, username):
            household = Household.query.filter_by(id=household).first()
            user = User.query.filter_by(username=username).first()
            if user is None:
                return jsonify(status="user_not_found"), 404
            household.creator = user.id
            self.db.session.commit()
            sid = general_socket_sid_mapping.get(user.username)
            if sid is not None:
                emit("ownership_received", {
                    "status": "ok",
                    "content": {
                        "household": household.id
                    }
                }, to=sid, namespace="/general")
            return jsonify(), 204


