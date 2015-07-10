#!/usr/bin/python 
# -*- coding: utf-8 -*-

import argparse
import sys
from cox_check import *


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--host')
args = parser.parse_args()
if args.host:
	cocaine_tool = cocaine_tool + ' -h ' + args.host


# Cocaine applications
apps_array = get_apps()

# Runlists
runlists_array = get_runlists()

apps_info = {}

# Get info about app
for app_name in apps_array:
	apps_info[app_name] = get_app_info(app_name)

apps_status = {}

for app_name in apps_info:
	state = get_app_state(app_name)

	if state == 'running':
		apps_status[app_name] = { '0': state }
	else:
		# Check production runlist
		runlist = get_runlist(runlists_array, app_name)
		if runlist == 'production':
			apps_status[app_name] = { '2': state }
		else:
			apps_status[app_name] = { '1': state }

crit_apps = []
warn_apps = []
for app in apps_status:
	for code in apps_status[app]:
		message = apps_status[app][code]
		if code == '2':
			crit_apps.append(app)
		if code == '1':
			warn_apps.append(app)

if len(crit_apps) == 0:
	pass
else:
	print crit_apps
	sys.exit(2)

if len(warn_apps) == 0:
	pass
else:
	print warn_apps
	sys.exit(1)

print "OK"
sys.exit(0)
