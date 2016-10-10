# ChatServer
Telnet Python Chat Server

Library:
- Python [Twisted][1]. 

Useage:
- Server : start the server with "python ChatServer.py". It will start on port 8988
- Client : connect with telnet to the server ip and port to start chatting. For example, "telnet 127.0.0.1 8988"

Commands:
- /users          ----- list all users
- /rooms          ----- list all rooms
- /create ROOM    ----- create single room
- /join ROOM      ----- join single room
- /leave          ----- leave your room
- /quit           ----- quit this chat application

[1]: http://twistedmatrix.com/trac/
