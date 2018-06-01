from __future__ import print_function
import os
import tweepy
import json
import unikovcode

creds_file = 'credentials.json'

credentials = {}

if os.path.isfile(creds_file):
    with open(creds_file) as infile:
        credentials = json.load(infile)
else:
    print('Credentials not found. Run auth_setup.py first.')
    exit(1)

auth = tweepy.OAuthHandler(credentials['ConsumerKey'],
                           credentials['ConsumerSecret'])
auth.set_access_token(credentials['AccessToken'],
                      credentials['AccessSecret'])

api = tweepy.API(auth)


def get_tweetable_codepoint():
    generator = unikovcode.get_generator()
    while True:
        codepoint = generator.generate()
        if len(codepoint) <= 140:
            return codepoint


def do_tweet(event, context):
    text = get_tweetable_codepoint()
    api.update_status(text)
    return text
