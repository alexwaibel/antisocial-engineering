#!/usr/bin/python3

import twitter, configparser, time

config = configparser.ConfigParser()
config.read('settings.cfg')

twitterEnabled = config['Twitter'].getboolean('enabled')

# Takes configparser as argument and connects API to account
def authenticateTwitter(config):
    consumerKey = str(config['Twitter']['consumer key'])
    consumerSecret = str(config['Twitter']['consumer secret'])
    accessToken = str(config['Twitter']['access token'])
    accessTokenSecret = str(config['Twitter']['access token secret'])

    twitterApi = twitter.Api(consumer_key=consumerKey,
                             consumer_secret=consumerSecret,
                             access_token_key=accessToken,
                             access_token_secret=accessTokenSecret)
    return twitterApi

# Takes a sequence of statuses and a number of days as the arguments. Deletes 
# every status that is older than the supplied number of days
def deleteOldTweets(statusSet, days):
    currentTime = int(time.time())
    SECONDS_IN_DAY = 86400
    daysAsSeconds = days * SECONDS_IN_DAY
    for status in statusSet:
        postTime = status.created_at_in_seconds
        if postTime < currentTime - daysAsSeconds:
            # twitterApi.DestroyStatus(status.id)
            print(twitterApi.GetStatus(status.text)),
    return

def main():
    if twitterEnabled:
        twitterApi = authenticateTwitter(config)
        print('Authenticated for Twitter user ' + twitterApi.VerifyCredentials().screen_name),

        statusSet = twitterApi.GetUserTimeline(exclude_replies=True,
                                            count=200,
                                            include_rts=True)

if __name__ == "__main__":
    main()

