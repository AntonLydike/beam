# Beam - a simple video streaming service

Two scripts for setting up local video streaming (audio might work aswell)

## Server
Run `server.py` with python3, the only dependency is flask and vlc player. This will open a server on port 5005, listening for these two routes: 

* `/open?host=<host>[&port=<port>]` This will run vlc on the server and attempt to stream from `http://<host>:<port>/stream` (default port is 4040). The response will contain the session ID that can be used to control the playback
* `/close/<id>` will close the vlc player from the specified connection id


## Client

Running `client.py <video file>` will create a symlink inside an empty temporary directory and start an http server there. Then it will call the `/open` API of the server specified in the `BEAM_SERVER` variable inside. Once evrything is running, it waits for any user input and will then clean up (stop the server, remove temp dir, call close on the server)