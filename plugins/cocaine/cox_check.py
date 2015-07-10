#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import ast

cocaine_tool = '/usr/bin/cocaine-tool'

# Get applications array
def get_apps():
    apps = get_cmd( cocaine_tool + ' app list' )
    apps_array = get_dict(apps)
    
    return apps_array


# Get runlists array
def get_runlists():
    runlists = get_cmd( cocaine_tool + ' runlist list' )
    runlists_array = get_dict(runlists)
    
    return runlists_array


# Return dictionary of cocaine applicatio info
def get_app_info(app_name):
	info 		= get_cmd( cocaine_tool + ' info -n ' + app_name )
	info_dict 	= get_dict(info)
	
	return info_dict


# Get application state
def get_app_state(app_name):
    app_info = get_app_info(app_name)
    state = ''
    try:
        state = app_info['apps'][app_name]['state']
    except:
        state = 'not running'
    
    return state


# Get dictionary from string
def get_dict(string):
	out_dict = ast.literal_eval(string)
	
	return out_dict


# Check runlis
def get_runlist(runlists, app):
	for runlist in runlists:
		runlist_info = get_runlist_info(runlist)
		try:
			if runlist_info[app]:
				return runlist
		except:
			pass
	
	return 'Not in runlist'


# Get runlist info
def get_runlist_info(runlist):
	info 		= get_cmd( cocaine_tool + ' runlist view -n ' + runlist )
	info_dict	= get_dict(info)
	
	return info_dict


# Get shell command output
def get_cmd(cmd):
	out = os.popen(cmd).read()
	
	return out

