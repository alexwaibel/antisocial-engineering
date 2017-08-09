#!/usr/bin/python3

import twitter, configparser

config = configparser.ConfigParser()
config.read('settings.cfg')

twitterEnabled = config['Twitter'].getboolean('enabled')

if twitterEnabled:
    consumerKey = str(config['Twitter']['consumer key'])
    consumerSecret = str(config['Twitter']['consumer secret'])
    accessToken = str(config['Twitter']['access token'])
    accessTokenSecret = str(config['Twitter']['access token secret'])

    twitterApi = twitter.Api(consumer_key=consumerKey,
                             consumer_secret=consumerSecret,
                             access_token_key=accessToken,
                             access_token_secret=accessTokenSecret)
    
    print('Authenticated for Twitter user ' + twitterApi.VerifyCredentials().screen_name)