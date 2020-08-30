import os
import sys
import socket
import secrets
import tempfile
import http.server
import socketserver

from threading import Thread
from urllib.request import urlopen

PORT = 4040
BEAM_SERVER = '192.168.0.3:5005'


d = tempfile.TemporaryDirectory()

print("using tempdir " + d.name)

def handler_for_dir(dir):
    def myhandler(*args, **kwargs):
        kwargs['directory'] = dir
        return http.server.SimpleHTTPRequestHandler(*args, **kwargs)

    return myhandler

def get_request(url):
    resp = urlopen(url)
    return (200 <= resp.status <= 299, "\n".join([d.decode() for d in resp.readlines()]))

# get ip address (sourced from https://stackoverflow.com/a/28950776/4141651)
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

target = sys.argv[1]

id = secrets.token_hex(16)

# symlink target to tempdir so we only expose a single file
os.symlink(os.path.abspath(target), d.name  + '/stream')

handler = handler_for_dir(d.name + '/')
token = None

try:
    with http.server.HTTPServer(("0.0.0.0", PORT), handler) as httpd:
        try:
            print("serving at port", PORT)
            t = Thread(target=httpd.serve_forever)
            t.start()
            print("calling beam target...")
            host = get_ip()
            resp = get_request(f'http://{BEAM_SERVER}/open?host={host}&port={PORT}')
            if resp[0]:
                token = resp[1].strip()
                print(f"successfully started video - session {token}")
                input("Just press enter when you are done...")
            else:
                print("Error statrtig video!")
        finally:
            print("shutting down server")
            httpd.shutdown()

finally:
    print("cleaning up")
    if token:
        get_request(f'http://{BEAM_SERVER}/stop/{token}')
    d.cleanup()
