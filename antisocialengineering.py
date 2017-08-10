#!/usr/bin/python3

import configparser
import sys
import time
import twitter

config = configparser.ConfigParser()
config.read('settings.cfg')

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


def deleteOldTweets(statusSet, days, api, exclusionList=[]):
    currentTime = int(time.time())
    SECONDS_IN_DAY = 86400
    daysAsSeconds = days * SECONDS_IN_DAY
    for status in statusSet:
        postTime = status.created_at_in_seconds
        if postTime < currentTime - daysAsSeconds and status.text.lower() not in exclusionList:
            api.DestroyStatus(status.id)
    return


def main():
    twitterEnabled = config['Twitter'].getboolean('enabled')

    if twitterEnabled:
        twitterApi = authenticateTwitter(config)
        print('Authenticated for Twitter user ' +
              twitterApi.VerifyCredentials().screen_name),

        excludeWords = config['General']['exclude key words'].split(",")
        [item.lower() for item in excludeWords]

        print('Deleting Twitter posts.'),
        lastStatusId = sys.maxsize
        statusSet = twitterApi.GetUserTimeline(exclude_replies=False,
                                               include_rts=True)
        while len(statusSet) > 0:
            lastStatusId = statusSet[len(statusSet) - 1].id
            deleteOldTweets(statusSet, int(
                config['Twitter']['days']), twitterApi, excludeWords)
            statusSet = twitterApi.GetUserTimeline(exclude_replies=False,
                                                   include_rts=True,
                                                   max_id=lastStatusId - 1)

        print('All posts older than ' + str(config['Twitter']['days']) +
              ' days have been deleted.'),


if __name__ == "__main__":
    main()
