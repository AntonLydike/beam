import secrets

from time import sleep
from flask import Flask, request
from subprocess import Popen, STDOUT, PIPE

SESSIONS = dict()

app = Flask(__name__)

@app.route('/open')
def open_stream():
    url = "http://" + request.args['host'] + ':' + request.args.get('port', '4040') + '/stream'
    id = secrets.token_hex(16)
    SESSIONS[id] = {
        'url': url,
        'id': id,
        'proc': Popen(['vlc', url])
    }
    return id

@app.route('/stop/<id>')
def stream_stop(id):
    if id in SESSIONS:
        SESSIONS[id]['proc'].terminate()
        return "true"
    return "false"

def cleanup_thread():
    while True:
        dead_sessions = []

        for session in SESSIONS.values():
            if session['proc'].poll() != None:
                # thread has terminated
                dead_sessions.append(session['id'])
        
        for id in dead_sessions:
            url = SESSIONS[id]['url']
            print(f"Removing dead session {id} for url {url}")
            del SESSIONS[id]
    
        sleep(10)

t = Thread(target=cleanup_thread)
t.start()
    
app.run(host='0.0.0.0', port=5005)