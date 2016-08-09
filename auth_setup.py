from __future__ import print_function
import os
import tweepy
import json
import subprocess

def write_creds(creds):
    with open(creds_file, 'w') as outfile:
        json.dump(creds, outfile)

creds_file = 'credentials.json'

credentials = {}

if os.path.isfile(creds_file):
    with open(creds_file) as infile:
        credentials = json.load(infile)
    if all(item in credentials for item in ['ConsumerKey', 'ConsumerSecret',
                                            'AccessToken', 'AccessSecret']):
        print('Nothing to do.')
        exit(0)

for item in ['ConsumerKey', 'ConsumerSecret']:
    if item not in credentials:
        credentials[item] = raw_input('%s: ' % item)

write_creds(credentials)

auth = tweepy.OAuthHandler(credentials['ConsumerKey'],
                           credentials['ConsumerSecret'])

auth_url = auth.get_authorization_url()

print('Go to:', auth_url)

verifier = raw_input('PIN: ')
credentials['AccessToken'], credentials['AccessSecret'] = auth.get_access_token(verifier)

write_creds(credentials)

print('Done')
