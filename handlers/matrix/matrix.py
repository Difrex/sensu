#!/usr/bin/python

from matrix_client.client import MatrixClient
import json
import fileinput

# Load config
c = open('/etc/sensu/handlers/notification/matrix.json', 'r')
c_j = c.read()
conf = json.loads(c_j)
c.close()

# Sensu event JSON
sensu_json = ''
for line in fileinput.input():
    sensu_json = sensu_json + line

sensu_event = None
try:
    sensu_event = json.loads(sensu_json)
except Exception as e:
    print(str(e))

# Status codes
statuses = {
    2: '**CRITICAL**: ',
    1: '*WARNING*: ',
    0: 'OK: '
}

# Event information
try:
    client = sensu_event['client']['name']
    check = sensu_event['check']['name']
    output = sensu_event['check']['output']
    status = statuses[sensu_event['check']['status']]
    history = sensu_event['check']['history']
except Exception as e:
    print(str(e))

previous_status = history[len(history)-1]

# Message text
# *WARNING*: Client_name\n /tmp/test does not exists
text = status + client + "\n" + output

# Check previous status and send check information
if previous_status != sensu_event['check']['status']:
    # Initialize Matrix client
    client = MatrixClient(conf['homeserver'])
    token = client.login_with_password(username=conf['username'],
                                       password=conf['password'])
    # Join to Room
    room = client.join_room(conf['room'])

    room.send_text(text)
