
SETTINGS = {
    'repositories': [
        'agri-hub/callisto-dataset-collection',
        'agri-hub/space2ground'
    ],
    'slack_channel_id': 'C02H6G73YTR', # replace with your own (this is not valid)
    # replace token with your own! The below is an example and not a valid one!
    'token': 'your-slackbot-token',
    'gh_url': 'https://api.github.com/repos',
}

# If you want to have redacted settings (e.g., have your application token
# automatically applied without it being visible publicly), you can create
# locally a "redacted.py" file, which is already git-ignored. In that file
# (which is attempted to be sourced right below), you can override the
# SETTINGS values. The following 2 lins are examples:
# """redacted.py"""
# SETTINGS['token']  = 'your-slackbot-token'
# SETTINGS['slack_channel_id'] = 'B39H42YRH3'
try:
    from redacted import *
except ImportError:
    print("No redacted overrides found ...")
