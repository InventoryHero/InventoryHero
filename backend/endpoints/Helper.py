from backend.db.models.User import HouseholdMembers


def user_in_household(user_id, household_id):
    household_member = HouseholdMembers.query.filter_by(member_id=user_id, household_id=household_id).first()
    if household_member is None:
        return False
    return True


