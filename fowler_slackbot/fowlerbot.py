import os
import time
from slackclient import SlackClient
import json
import string
import argparse
import pprint
import sys

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
SLACK_BOT_TOKEN = 'xoxb-149796404210-BBk15oz9YGqHeJE4BtLpJVhE'
slack_client = SlackClient(SLACK_BOT_TOKEN)
USERS = slack_client.api_call("users.list")
not_letters_or_digits = u'!"#%()*+,-./:\';<=>?@[\]^_`{|}~\u2019\u2026\u201c\u201d\xa0'
translate_table = dict((ord(char), u'') for char in not_letters_or_digits)

def handle_command(user, text, service, flags):
	papi = service.trainedmodels()
	text = text.translate(translate_table)
	body = {'input': {'csvInstance': [text]}}
	result = papi.predict(body=body, id=flags.model_id, project=flags.project_id).execute()
	print float(result[u'outputValue'])

def parse_slack_output(slack_rtm_output):
  output_list = slack_rtm_output
  if output_list and len(output_list) > 0:
      for output in output_list:
      	try:
      		for member in USERS['members']:
      			try: 
        			if member['id'] == output['user']:
        				return member['name'], \
        							 output['text'].strip().lower()
        		except Exception:
      				pass
      	except Exception:
      		pass
  return None, None

def main(argv):
	READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
	service, flags = sample_tools.init(
		argv, 'prediction', 'v1.6', __doc__, __file__, parents=[argparser],
		scope=(
		  'https://www.googleapis.com/auth/prediction',
		  'https://www.googleapis.com/auth/devstorage.read_only'))
	if slack_client.rtm_connect():
		print("FowlerBot connected and running!")
		while True:
			user, text = parse_slack_output(slack_client.rtm_read())
			if user and text:
				handle_command(user, text, service, flags)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed. Invalid Slack token or bot ID?")


if __name__ == "__main__":
	main(sys.argv)
   