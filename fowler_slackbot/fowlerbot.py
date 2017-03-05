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



# sqlite config
def db_conn():
	sqldb = "user.db"
	sqltable = "users"
	schema = "(user, userid, num_violations)"
	fileout = "./sqlout.csv"
	
	conn = sqlite3.connect(sqldb)
	sql = conn.cursor()
	sql.execute("CREATE TABLE IF NOT EXISTS " + sqltable + " " + schema)
	dbconfig = {
		"conn": conn,
		"sql": sql,
		"sqltable": sqltable,
		"schema": schema,
		"fileout": fileout
	}
	sql.execute("SELECT user, num_violations FROM " + sqltable + " ORDER BY num_violations DESC")
	output_data = sql.fetchall()
	output_data = output_data[:5]
	print output_data
	db_post_output(output_data)
	return dbconfig

def db2_conn():
	sqldb = "user.db"
	sqltable = "accusations"
	schema = "(user, userid, num_violations)"
	fileout = "./accusations.csv"
	conn = sqlite3.connect(sqldb)
	sql = conn.cursor()
	sql.execute("CREATE TABLE IF NOT EXISTS " + sqltable + " " + schema)
	dbconfig = {
		"conn": conn,
		"sql": sql,
		"sqltable": sqltable,
		"schema": schema,
		"fileout": fileout
	}
	sql.execute("SELECT user, num_violations FROM " + sqltable + " ORDER BY num_violations DESC")
	output_data = sql.fetchall()
	output_data = output_data[:5]
	print output_data
	db_post_output2(output_data)
	return dbconfig

def db_post_output(output_data):
	try:
		r = requests.post('http://localhost:3000/data', data={'data': output_data})
	except Exception as e:
		print e

def db_post_output2(output_data):
	try:
		r = requests.post('http://localhost:3000/reported', data={'data': output_data})
	except Exception as e:
		print e

def db_execute(dbconfig, user, userid):
	conn = dbconfig["conn"]
	sql = dbconfig["sql"]
	sqltable = dbconfig["sqltable"]
	sql.execute("SELECT * FROM " + sqltable + " WHERE userid='" + userid.encode('ascii') + "'")
	user_data = sql.fetchone()
	sql.execute("DELETE FROM " + sqltable + " WHERE userid='" + userid.encode('ascii') + "'")
	if user_data == None:
		user_data = (user.encode('ascii'),userid.encode('ascii'),1)
		
	user_data = (user_data[0].encode('ascii'),user_data[1].encode('ascii'),user_data[2]+1)
	sql.execute("INSERT INTO " + sqltable + " VALUES " + str(user_data))
	
	print user_data
	conn.commit()
	
	#get top 5
	sql.execute("SELECT user, num_violations FROM " + sqltable + " ORDER BY num_violations DESC")
	output_data = sql.fetchall()
	output_data = output_data[:5]
	print output_data
	db_post_output(output_data)

def db_accusations(dbconfig, user, userid):
	conn = dbconfig["conn"]
	sql = dbconfig["sql"]
	sqltable = dbconfig["sqltable"]
	sql.execute("SELECT * FROM " + sqltable + " WHERE userid='" + userid.encode('ascii') + "'")
	user_data = sql.fetchone()
	sql.execute("DELETE FROM " + sqltable + " WHERE userid='" + userid.encode('ascii') + "'")
	if user_data == None:
		user_data = (user.encode('ascii'),userid.encode('ascii'),1)
		
	user_data = (user_data[0].encode('ascii'),user_data[1].encode('ascii'),user_data[2]+1)
	sql.execute("INSERT INTO " + sqltable + " VALUES " + str(user_data))
	
	print user_data
	conn.commit()
	
	#get top 5
	sql.execute("SELECT user, num_violations FROM " + sqltable + " ORDER BY num_violations DESC")
	output_data = sql.fetchall()
	output_data = output_data[:5]
	print output_data
	db_post_output2(output_data)

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
TRESHOLD = 0.07

COMMANDS = {
    "offenders"	: "Fowlerbot will show the top offenders"
}

def list_offenders(channel):
		response = "Top offenders are: "
		slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def handle_command(user, userid,  text, service, flags, channel, dbconfig):
	if text == "<@u4dpebw66>: offenders":
			list_offenders(channel)
			return
	papi = service.trainedmodels()
	text = text.translate(translate_table)
	body = {'input': {'csvInstance': [text]}}
	result = papi.predict(body=body, id=flags.model_id, project=flags.project_id).execute()
	value = float(result[u'outputValue'])
	if value > TRESHOLD:
		response = "<@" + userid + "> said something inappropriate. Confidence level (0 to 1) is: " + str(max(0, min(1, value)))+ ". This violation has been logged."
		slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
		
		db_execute(dbconfig, user, userid)

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
				db_accusations(dbconfig, member['name'], member['id'])
		except Exception:
			pass

def main(argv):
	dbconfig = db_conn()
	dbconfig2 = db2_conn()
	READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
	service, flags = sample_tools.init(
		argv, 'prediction', 'v1.6', __doc__, __file__, parents=[argparser],
		scope=(
		  'https://www.googleapis.com/auth/prediction',
		  'https://www.googleapis.com/auth/devstorage.read_only'))
	if slack_client.rtm_connect():
		print("FowlerBot connected and running!")
		while True:
			user, userid,  text, channel = parse_slack_output(slack_client.rtm_read())
			if channel == 'D4D3GBG0Z':
				sexual_harassment_complaint(text, userid, dbconfig2)
			elif user and text:
				handle_command(user, userid, text, service, flags, channel, dbconfig)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed. Invalid Slack token or bot ID?")


if __name__ == "__main__":
	main(sys.argv)