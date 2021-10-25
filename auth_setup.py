from __future__ import print_function
import os
import tweepy
import json

try:
    input = raw_input
except NameError:
    pass


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


print('Input credentials from https://apps.twitter.com/')
for item in ['ConsumerKey', 'ConsumerSecret']:
    if item not in credentials:
        credentials[item] = input('%s: ' % item)

write_creds(credentials)

auth = tweepy.OAuthHandler(credentials['ConsumerKey'],
                           credentials['ConsumerSecret'])

auth_url = auth.get_authorization_url()

print('Go here to get PIN:')
print(auth_url)

verifier = input('PIN: ')
credentials['AccessToken'], credentials['AccessSecret'] = auth.get_access_token(
    verifier)

write_creds(credentials)

print('Done')
