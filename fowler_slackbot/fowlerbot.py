import os
import time
from slackclient import SlackClient
import json

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
USERS = slack_client.api_call("users.list")

def handle_command(user, text):
	


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

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("FowlerBot connected and running!")
        while True:
            user, text = parse_slack_output(slack_client.rtm_read())
            if user and text:
              handle_command(user, text)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")