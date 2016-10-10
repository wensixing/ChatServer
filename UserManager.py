
class UserManager:
    def __init__(self):
        self.users = {}  # maps user names to Chat instances
        self.room_users = {}  # maps room to user names
        self.user_room = {}  # maps user name to room

    def if_user_exist(self, name):
        if name in self.users:
            return True
        return False

    def get_all_rooms(self):
        return self.room_users

    def get_all_users(self):
        return self.users;

    def add_user(self, name, chat):
        self.users[name] = chat

    def if_room_exist(self, room):
        if room in self.room_users:
            return True
        return False

    def add_room(self, room):
        self.room_users[room] = set()

    def add_user_to_room(self, room, name):
        self.room_users[room].add(name)
        self.user_room[name] = room

    def get_user_chat(self, name):
        if self.if_user_exist(name):
            return self.users[name]

    def get_user_room(self, name):
        if name in self.user_room:
            return self.user_room[name]

    def get_room_users(self, room):
        if room in self.room_users:
            return self.room_users[room]

    def leave_room(self, name):
        if name not in self.user_room:
            return
        room = self.user_room[name]
        del self.user_room[name]
        self.room_users[room].remove(name)
        self.__check_empty_room(room)

    def remove_user(self, name):
        if not self.if_user_exist(name):
            return
        del self.users[name]
        if name in self.user_room:
            room = self.user_room[name]
            del self.user_room[name]
            self.__check_empty_room(room)

    def __check_empty_room(self, room):
        if not self.room_users[room]:
            del self.room_users[room]
