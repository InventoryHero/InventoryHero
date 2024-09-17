class SidManager:
    def __init__(self):
        self._user_to_sid = {}

    def add(self, username, sid):
        self._user_to_sid[username] = sid

    def remove(self, username):
        self._user_to_sid.pop(username, None)

    def get(self, username):
        return self._user_to_sid.get(username, None)


general_socket_sid_mapping = SidManager()

