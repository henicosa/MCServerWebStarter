from flask import Flask, Response, render_template, jsonify
from flask_basicauth import BasicAuth

import time

import json

def read_json(path):
    with open(path) as f:
        return json.load(f)

app = Flask(__name__)

secrets = read_json("secrets/secrets.json")
settings = read_json("application.json")

server_start_webhook_url = secrets["server_start_webhook_url"]
minecraft_server_address = secrets["minecraft_server_address"]
server_address = minecraft_server_address.split(":")[0]

last_time_executed = 0

app.config['BASIC_AUTH_USERNAME'] = secrets['username']
app.config['BASIC_AUTH_PASSWORD'] = secrets['password']

basic_auth = BasicAuth(app)

program_status = "not running"

'''
-----------------------------------------------------

Section for App-specific functions

-----------------------------------------------------
'''

# to do

'''
-----------------------------------------------------

Section for template functions

-----------------------------------------------------
'''

@app.route('/')
def index():
    return render_template('index.html', **read_json("application.json"))

@app.route('/secret')
@basic_auth.required
def secret_page():
    return "You have access to the secret page!"

@app.route('/status')
def status():
    global program_status
    if time.time() - last_time_executed < 10:
        program_status = "starting"
    else:
        if is_computer_online(server_address):
            if is_minecraft_server_running(minecraft_server_address):
                program_status = "success"
            else:
                program_status = "starting"
        else:
            program_status = "not running"
    return jsonify(status=program_status)

@app.route('/logs')
@basic_auth.required
def logs():
    log_messages = []
    with open('app/log/application.log', 'r') as logfile:
        for line in logfile:
            try:
                time, application, log_type, message = line.strip().split(' ', 3)
                log_messages.append({'time': time, 'application': application, 'type': log_type, 'message': message})
            except Exception as e:
                print("Parse Error for log event:" + line)
    log_messages = log_messages[::-1]  # Reverse the order of the messages to display the latest message first
    return render_template('logs.html', log_messages=log_messages)


@app.route('/activate', methods=['POST'])
def activate():
    global program_status
    if program_status == "success":
        return jsonify(status='already running')
    if program_status != "starting":
        if start():
            program_status = "starting"
        else:
            program_status = "failed"
    return jsonify(status=program_status)



import os
def is_computer_online(ip_address, timeout=100):
    print("Ping computer at", ip_address)

    response = os.system("ping -c 1 -W 4 " + ip_address)

    #and then check the response...
    if response == 0:
        return True
    else:
        return False


from mcstatus import JavaServer
def is_minecraft_server_running(minecraft_server_address):
    server = JavaServer.lookup(minecraft_server_address)
    try:
        status = server.status()
        print("Server is running")
        return True
    except Exception as e:
        print("Server is not running")
        return False

import requests
def start():
    global last_time_executed
    try:
        # send post request and return true if successful
        r = requests.post(server_start_webhook_url)
        if r.status_code == 200:
            print("Server accepted request")
            last_time_executed = time.time()
            return True
        else:
            print("Error: " + str(r.status_code))
            return False
    except Exception as e:
        print("Error: " + str(e))
        return False

if __name__ == '__main__':
    app.run()