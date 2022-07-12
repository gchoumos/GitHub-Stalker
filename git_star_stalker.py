import logging
import requests
import json
import os

import pdb

from settings import SETTINGS

# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
client = WebClient(token=SETTINGS['token'])
logger = logging.getLogger(__name__)
channel_id = SETTINGS['slack_channel_id']
repos = SETTINGS['repositories']
base_url = SETTINGS['gh_url']

# Load the previously known status of the repository
with open('repo-status.json') as json_file:
    previous_status = json.load(json_file)

current_status = {}
for repo in repos:
    # Get previously known stats

    # stars
    try:
        previous_stars = previous_status[repo]['stars']
    except KeyError:
        previous_stars = 0

    # forks
    try:
        previous_forks = previous_status[repo]['forks']
    except KeyError:
        previous_forks = 0

    # subs (watchers)
    try:
        previous_subs = previous_status[repo]['subs']
    except KeyError:
        previous_subs = 0
  

    # Get the current status for this repo from GitHub
    url = '{0}/{1}'.format(base_url,repo)
    r = requests.get(url)

    # load the response as a python dictionary
    response = json.loads(r.text)

    # pdb.set_trace()
    current_status[repo] = {}
    current_status[repo]['stars'] = response['stargazers_count']
    current_status[repo]['forks'] = response['forks_count']
    current_status[repo]['subs']  = response['subscribers_count']


# We got the current status of our repos. Time to collect updates (if any exist)
updates = (previous_status != current_status) # will be true if updates exist

if not updates:
    slack_messages =  ['No updates detected in the monitored repositories']
else:
    slack_messages =  ['GitHub Repository Updates']
    slack_messages.append('')

for repo in repos:
    # Will be true if updates exist
    repo_updates = previous_status[repo] != current_status[repo]

    if repo_updates:
        slack_messages.append('\t{0}'.format(repo))

    if current_status[repo]['stars'] != previous_status[repo]['stars']:
        slack_messages.append('\t\tStars: {0} --> {1}'.format(
                previous_status[repo]['stars'],
                current_status[repo]['stars']
            )
        )

    if current_status[repo]['forks'] != previous_status[repo]['forks']:
        slack_messages.append('\t\tForks: {0} --> {1}'.format(
                previous_status[repo]['forks'],
                current_status[repo]['forks']
            )
        )

    if current_status[repo]['subs'] != previous_status[repo]['subs']:
        slack_messages.append('\t\tSubs: {0} --> {1}'.format(
                previous_status[repo]['subs'],
                current_status[repo]['subs']
            )
        )

try:
    if updates or SETTINGS['slack_no_updates']:
        slack_message = '\n'.join(slack_messages)

        result = client.chat_postMessage(
          channel=channel_id,
          text=slack_message
        )
        print(result)

    # Update the current status by saving it to the json file

    # remove previous backup (if exists)
    if os.path.exists("repo-status.json.bak"):
        os.remove("repo-status.json.bak")
        print("Previous backup removed")

    # move current status to previous status
    os.rename('repo-status.json', 'repo-status.json.bak')

    # save new status
    with open('repo-status.json', 'w') as fp:
        json.dump(current_status, fp)

except SlackApiError as e:
    print(f"Error: {e}")

