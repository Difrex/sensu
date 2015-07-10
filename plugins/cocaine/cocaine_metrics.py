#!/usr/bin/python 
# -*- coding: utf-8 -*-

import time
import socket
from cox_check import get_apps, get_app_info, get_app_state

apps = get_apps()
hostname = socket.getfqdn()

for app in apps:
    status = get_app_state(app)
    if status == 'running':
        info = get_app_info(app)
        print hostname + '.' + app + ".load-median "            + str( info['apps'][app]['load-median'] )               + ' ' + str ( time.time() )
        print hostname + '.' + app + ".sessions.pending "       + str( info['apps'][app]['sessions']['pending'] )       + ' ' + str ( time.time() )
        print hostname + '.' + app + ".queue.depth "            + str( info['apps'][app]['queue']['depth'] )            + ' ' + str ( time.time() )
        print hostname + '.' + app + ".queue.capacity "         + str( info['apps'][app]['queue']['capacity'] )         + ' ' + str ( time.time() )
        print hostname + '.' + app + ".slaves.active "          + str( info['apps'][app]['slaves']['active'] )          + ' ' + str ( time.time() )
        print hostname + '.' + app + ".slaves.idle "            + str( info['apps'][app]['slaves']['idle'] )            + ' ' + str ( time.time() )
        print hostname + '.' + app + ".slaves.capacity "        + str( info['apps'][app]['slaves']['capacity'] )        + ' ' + str ( time.time() )


#{
#    "apps": {
#        "js": {
#            "load-median": 0, 
#            "profile": "default", 
#            "sessions": {
#                "pending": 0
#            }, 
#            "queue": {
#                "depth": 0, 
#                "capacity": 100
#            }, 
#            "state": "running", 
#            "slaves": {
#                "active": 0, 
#                "idle": 0, 
#                "capacity": 10
#            }
#        }
#    }
#}
