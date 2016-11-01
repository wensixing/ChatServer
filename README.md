# ChatServer
Telnet Python Chat Server

Library:
- Python [Twisted][1]. 

Usage:
- Server : start the server with "python ChatServer.py". It will start on port 8988
- Client : connect with telnet to the server ip and port to start chatting.
Server:
```
python ChatServer.py
```
Client:
```
Telnet SERVER_IP 8988
```



Controll:

| Commands      | Discription      |
| ------------- |:-------------|
| /users      | list all users |
| /rooms      | list all rooms      |
| /create ROOM | create a single room      |
| /join ROOM  | join a single room      |
| /leave | leave your room      |
| /quit | quit this chat application      |
| /whisper USER | send USER a private message     |



[1]: http://twistedmatrix.com/trac/
