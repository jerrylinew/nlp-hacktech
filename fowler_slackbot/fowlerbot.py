import os
import time
from slackclient import SlackClient
import json
import string
import argparse
import pprint
import sys
import sqlite3
import httplib
import urllib
import base64

import requests

from apiclient import discovery
from apiclient import sample_tools
from oauth2client import client

argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('object_name',
    help='Full Google Storage path of csv data (ex bucket/object)')
argparser.add_argument('model_id',
    help='Model Id of your choosing to name trained model')
argparser.add_argument('project_id',
    help='Project Id of your Google Cloud Project')

sys.path.insert(1, '/Library/Python/2.7/site-packages')



def db_init(dbconfig):
	sql = dbconfig["sql"]
	sqltable = dbconfig["sqltable"]
	schema = dbconfig["schema"]
	sql.execute("CREATE TABLE IF NOT EXISTS " + sqltable + " " + schema)

# sqlite config
def db_conn():
	sqldb = "user.db"
	conn = sqlite3.connect(sqldb)
	sql = conn.cursor()
	
	dbconfig_redflags = {
		"conn": conn,
		"sql": sql,
		"sqltable": "red_flags",
		"schema": "(user, userid, num_violations)",
		"endpoint": "/data"
	}
	
	dbconfig_accusations = {
		"conn": conn,
		"sql": sql,
		"sqltable": "accusations",
		"schema": "(user, userid, num_violations)",
		"endpoint": "/reported"
	}

	dbconfig_messages = {
		"conn": conn,
		"sql": sql,
		"sqltable": "messages",
		"schema": "(user, userid, message, score)",
		"endpoint": "/messages"
	}
	
	db_init(dbconfig_redflags)
	db_init(dbconfig_accusations)
	db_init(dbconfig_messages)

	sql.execute("SELECT user, userid, num_violations FROM " + dbconfig_redflags["sqltable"] + " ORDER BY num_violations DESC")
	redflags_data = sql.fetchall()[:5]
	print redflags_data
	db_post_output(redflags_data, dbconfig_redflags["endpoint"])

	sql.execute("SELECT user, userid, num_violations FROM " + dbconfig_accusations["sqltable"] + " ORDER BY num_violations DESC")
	accusation_data = sql.fetchall()[:5]
	print accusation_data
	db_post_output(accusation_data, dbconfig_accusations["endpoint"])

	messages_data = {"data": []}
	for x in redflags_data:
		sql.execute("SELECT user, message, score FROM " + dbconfig_messages["sqltable"] + " WHERE userid='" + x[1] + "' ORDER BY score DESC")
		messages_data["data"] = messages_data["data"] + sql.fetchall()[:5]
	db_post_output(messages_data, dbconfig_messages["endpoint"])

	return dbconfig_redflags, dbconfig_accusations, dbconfig_messages

def db_post_output(output_data, endpoint):
	try:
		r = requests.post('http://localhost:3000' + endpoint, data={'data': output_data})
	except Exception as e:
		print e

def db_execute(dbconfig, user, userid, incr):
	conn = dbconfig["conn"]
	sql = dbconfig["sql"]
	sqltable = dbconfig["sqltable"]
	sql.execute("SELECT * FROM " + sqltable + " WHERE userid='" + userid.encode('ascii') + "'")
	user_data = sql.fetchone()
	sql.execute("DELETE FROM " + sqltable + " WHERE userid='" + userid.encode('ascii') + "'")
	if user_data == None:
		user_data = (user.encode('ascii'),userid.encode('ascii'),0)

	user_data = (user_data[0].encode('ascii'),user_data[1].encode('ascii'),user_data[2]+incr)
	sql.execute("INSERT INTO " + sqltable + " VALUES " + str(user_data))

	conn.commit()

	#get top 5
	sql.execute("SELECT user, userid, num_violations FROM " + sqltable + " ORDER BY num_violations DESC")
	output_data = sql.fetchall()
	output_data = output_data[:5]

	db_post_output(output_data, dbconfig["endpoint"])
	return output_data

def db_metadata(dbconfig):
	conn = dbconfig["conn"]
	sql = dbconfig["sql"]
	sqltable = dbconfig["sqltable"]

	sql.execute("SELECT * FROM " + dbconfig["sqltable"])
	num_msgs = len(sql.fetchall())
	sql.execute("SELECT * FROM " + dbconfig["sqltable"] + " WHERE score > " + str(THRESHOLD))
	num_fmsgs = len(sql.fetchall())
	sql.execute("SELECT DISTINCT user FROM " + dbconfig["sqltable"])
	num_users = len(sql.fetchall())
	sql.execute("SELECT DISTINCT user FROM " + dbconfig["sqltable"] + " WHERE score > " + str(THRESHOLD))
	num_fusers = len(sql.fetchall())

	metadata = {"data": (num_msgs, num_fmsgs, num_users, num_fusers)}
	db_post_output(metadata, "/metadata")

def db_add_msg(dbconfig, msgdata, redflags_data):
	conn = dbconfig["conn"]
	sql = dbconfig["sql"]
	sqltable = dbconfig["sqltable"]

	msgdata = (msgdata[0].encode('ascii'), msgdata[1].encode('ascii'), msgdata[2].encode('ascii'), msgdata[3])
	sql.execute("INSERT INTO " + sqltable + " VALUES " + str(msgdata))

	#get flagged msg of top 5
	print redflags_data
	messages_data = {"data": []}
	for x in redflags_data:
		sql.execute("SELECT user, message, score FROM " + dbconfig["sqltable"] + " WHERE userid='" + x[1] + "' ORDER BY score DESC")
		messages_data["data"] = messages_data["data"] + sql.fetchall()[:5]
	print messages_data
	db_post_output(messages_data, dbconfig["endpoint"])

def print_header(line):
	'''Format and print header block sized to length of line'''
	header_str = '='
	header_line = header_str * len(line)
	print('\n' + header_line)
	print(line)
	print(header_line)

# starterbot's ID as an environment variable
BOT_ID = 'U4DPEBW66'

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
# instantiate Slack & Twilio clients
SLACK_BOT_TOKEN = os.environ['SLACK_KEY']
slack_client = SlackClient(SLACK_BOT_TOKEN)
USERS = slack_client.api_call("users.list")
not_letters_or_digits = u'!"#%()*+,-./:\';<=>?@[\]^_`{|}~\u2019\u2026\u201c\u201d\xa0'
translate_table = dict((ord(char), u'') for char in not_letters_or_digits)
THRESHOLD = 0.07

COMMANDS = {
    "offenders"	: "Fowlerbot will show the top offenders"
}

def list_offenders(channel):
		response = "Top offenders are: "
		slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def handle_command(user, userid,  text, service, flags, channel, dbconfig_redflags, dbconfig_messages):
	if user == "fowler_bot":
			return
	if text == "<@u4dpebw66>: offenders":
			list_offenders(channel)
			return
	papi = service.trainedmodels()
	text = text.translate(translate_table)
	body = {'input': {'csvInstance': [text]}}
	result = papi.predict(body=body, id=flags.model_id, project=flags.project_id).execute()
	value = float(result[u'outputValue'])

	incr = 0
	if value > THRESHOLD:
		response = "<@" + userid + "> said something inappropriate. Confidence level (0 to 1) is: " + str(max(0, min(1, value)))+ ". This violation has been logged."
		slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
		
		incr = 1
	redflags_data = db_execute(dbconfig_redflags, user, userid, incr)
	db_add_msg(dbconfig_messages, (user, userid, text, value), redflags_data)
	db_metadata(dbconfig_messages)



def parse_slack_output(slack_rtm_output):
	output_list = slack_rtm_output
	if output_list and len(output_list) > 0:
		for output in output_list:
			try:
				for member in USERS['members']:
					try:
						if member['id'] == output['user']:
							return member['name'], \
									 member['id'], \
        							 output['text'].strip().lower(), \
									 output['channel']
					except Exception:
						pass
			except Exception:
				pass
	return None, None, None, None

def sexual_harassment_complaint(text, userid, dbconfig):
	for member in USERS['members']:
		try:
			if member['name'] in text:
				print member['name'] + " is accused of sexual harassment"
				db_execute(dbconfig, member['name'], member['id'], 1)
		except Exception:
			pass

def main(argv):
	dbconfig_redflags, dbconfig_accusations, dbconfig_messages = db_conn()
	READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
	service, flags = sample_tools.init(
		argv, 'prediction', 'v1.6', __doc__, __file__, parents=[argparser],
		scope=(
		  'https://www.googleapis.com/auth/prediction',
		  'https://www.googleapis.com/auth/devstorage.read_only'))
	if slack_client.rtm_connect():
		print("FowlerBot connected and running!")
		while True:
			user, userid, text, channel = parse_slack_output(slack_client.rtm_read())
			if channel:
				sexual_harassment_complaint(text, userid, dbconfig_accusations)
			if user and text:
				handle_command(user, userid, text, service, flags, channel, dbconfig_redflags, dbconfig_messages)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed. Invalid Slack token or bot ID?")


if __name__ == "__main__":
	main(sys.argv)