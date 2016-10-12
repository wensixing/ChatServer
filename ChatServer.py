from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from UserManager import UserManager


class Chat(LineReceiver):

    def __init__(self, user_manager):
        self.user_manager = user_manager
        self.name = None
        self.room = None
        self.whisper_user = None
        self.state = "INIT"
        self.cmd = {"/users", "/create", "/rooms", "/join", "/leave", "/quit", "/help", "/whisper"}

    def is_command(self, line):
        cmd = line.split(' ')
        if cmd[0] in self.cmd:
            return True
        return False

    def connectionMade(self):
        self.sendLine("[System] Welcome to NA chat")
        self.sendLine("[System] Login name ?")

    def connectionLost(self, reason):
        self.user_manager.remove_user(self.name)

    def lineReceived(self, line):
        if self.state == "INIT":
            self.get_name(line)
        elif self.state == "CHAT":
            if len(line) > 0:
                if self.is_command(line):
                    self.exe_cmd(line)
                else:
                    self.handle_msg(line)
        self.sendLine("")

    def exe_cmd(self, command):
        cmd = command.split(' ')
        if len(cmd) == 0:
            return
        if cmd[0] == "/users":
            self.show_users_list()
        elif cmd[0] == "/create":
            self.create_room(cmd[1])
        elif cmd[0] == "/whisper":
            self.whisper(cmd[1])
        elif cmd[0] == "/rooms":
            self.show_rooms_list()
        elif cmd[0] == "/join":
            if len(cmd) != 2:
                self.wrong_cmd()
                return
            self.join_room(cmd[1])
        elif cmd[0] == "/leave":
            if not self.room:
                return
            self.leave_room()
        elif cmd[0] == "/quit":
            self.sendLine("[System] BYE !")
            self.quit()
        elif cmd[0] == "/help":
            self.help_list()

    def whisper(self, name):
        if self.name == name:
            self.sendLine("[System] Can not whisper to yourself")
            return
        elif not self.user_manager.if_user_exist(name):
            self.sendLine("[System] No this user")
            return
        self.sendLine("[System] Your next message will be sent to %s" % (name,))
        self.whisper_user = name

    def quit(self):
        if self.room:
            self.leave_room()
        self.user_manager.remove_user(self.name)
        self.transport.loseConnection()

    def join_room(self, room):
        if not self.user_manager.if_room_exist(room):
            self.sendLine("[System] No such room")
            return
        self.room = room
        self.user_manager.add_user_to_room(self.room, self.name)
        self.sendLine("[System] You have joined chat %s" % (self.room, ))
        message = " * New user joined chat: %s" % (self.name,)
        self.send_to_room(message)

    def show_rooms_list(self):
        rooms = self.user_manager.get_all_rooms()
        message = ""
        if len(rooms) > 0:
            message = "[System] Active rooms are \n"
            for room, users in rooms.iteritems():
                message += "[System] * %s (%s) \n" % (room, len(users))
            message += "[System] end of list"
        else:
            message = "[System] No room"
        self.sendLine(message)

    def show_users_list(self):
        users = self.user_manager.get_all_users()
        message = "[System] Active users are \n"
        for name, protocol in users.iteritems():
            if name != self.name:
                message += "[System] * " + name + "\n"
            else:
                message += "[System] * " + name + " (this is you ^ ^)\n"
        message += "[System] end of list"
        self.sendLine(message)

    def wrong_cmd(self):
        self.sendLine("[System] Wrong cmd !")
        self.help_list()

    def help_list(self):
        self.sendLine("[System] Chat commands are blow !")
        self.sendLine("/users                   ----- list all users")
        self.sendLine("/rooms                   ----- list all rooms")
        self.sendLine("/create ROOM             ----- create single room")
        self.sendLine("/join ROOM               ----- join single room")
        self.sendLine("/leave                   ----- leave your room")
        self.sendLine("/quit                    ----- quit this chat application")
        self.sendLine("/whisper USER            ----- send USER a private message")

    def create_room(self, room):
        if self.room:
            self.sendLine("[System] You have to leave this room at first")
            return
        self.user_manager.add_room(room)
        self.sendLine("[System] Room %s has been created" % room)
        self.join_room(room)

    def leave_room(self):
        message = " * User has left chat: %s" % (self.room,)
        self.send_to_room(message)
        self.user_manager.leave_room(self.name)
        self.room = None

    def get_name(self, name):
        if self.user_manager.if_user_exist(name):
            self.sendLine("[System] Name taken, please choose another.")
            self.sendLine("[System] Login name ?")
            return
        self.sendLine("[System] Welcome, %s!" % (name,))
        self.name = name
        self.user_manager.add_user(name, self)
        self.state = "CHAT"

    def handle_msg(self, message):
        if self.whisper_user:
            self.send_whisper(message)
            self.sendLine("[System] Whisper sent")
        elif self.room:
            self.send_to_users(self.user_manager.get_room_users(self.room), message)
            self.sendLine("[System] Room message sent")
        else:
            self.wrong_cmd()

    def send_to_room(self, message):
        users_in_room = self.user_manager.get_room_users(self.room)
        if not users_in_room:
            return
        self.send_to_users(users_in_room, message)

    def send_whisper(self, message):
        msg = "[Whisper] <%s> %s" % (self.whisper_user, message)
        protocol = self.user_manager.get_user_chat(self.whisper_user)
        if protocol != self:
            protocol.sendLine(msg)
        self.whisper_user = None

    def send_to_users(self, users, message):
        msg = "[Room] <%s> %s" % (self.name, message)
        for name in users:
            protocol = self.user_manager.get_user_chat(name)
            if protocol != self:
                protocol.sendLine(msg)


class ChatFactory(Factory):

    def __init__(self):
        self.user_manager = UserManager()

    def buildProtocol(self, addr):
        return Chat(self.user_manager)



reactor.listenTCP(8988, ChatFactory())
reactor.run()