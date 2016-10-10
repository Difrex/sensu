from matrix_client.client import MatrixClient
import json
import sys

# Load config
conf = json.load('/etc/sensu/handlers/notifications/matrix.json')

# Sensu event JSON
sensu_json = sys.stdin.read()
sensu_event = json.loads(sensu_json)

# Status codes
statuses = {
    '2': '**CRITICAL**: ',
    '1': '*WARNING*: ',
    '0': 'OK: '
}

# Event information
client = sensu_event['client']['name']
check = sensu_event['check']['name']
output = sensu_event['check']['output']
status = statuses[sensu_event['check']['status']]

# Message text
text = status + client + "\n" + output

# Initialize Matrix client
client = MatrixClient(conf['homeserver'])
token = client.login_with_password(username=conf['username'],
                                   password=conf['password'])
# Join to Room
room = client.join_room(conf['room'])

room.send_text(text)
