#!/usr/bin/python3

"""antisocialengineering.py

This module deletes posts on various social media platforms after they have
been up for a specified number of days.

"""

import configparser
import sys
import time
import twitter

CONFIG = configparser.ConfigParser()
CONFIG.read('settings.cfg')
SECONDS_IN_DAY = 86400

def authenticate_twitter(config):
    """Function that takes configparser object as an argument and connects
    to the API to the twitter account whose credentials are specified in the
    settings.cfg file
    """


    user_consumer_key = str(config['Twitter']['consumer key'])
    user_consumer_secret = str(config['Twitter']['consumer secret'])
    user_access_token = str(config['Twitter']['access token'])
    user_access_token_secret = str(config['Twitter']['access token secret'])

    twitter_api = twitter.Api(consumer_key=user_consumer_key,
                              consumer_secret=user_consumer_secret,
                              access_token_key=user_access_token,
                              access_token_secret=user_access_token_secret)
    return twitter_api

def delete_old_tweets(status_set, days, api, exclusion_list=None):

    """Deletes every status that is older than the supplied number of days.
    Posts with words found in exclusion_list are not deleted.
    """

    current_time = int(time.time())
    days_as_seconds = days * SECONDS_IN_DAY
    if exclusion_list is  None:
        exclusion_list = []
    for status in status_set:
        post_time = status.created_at_in_seconds
        if post_time < current_time - days_as_seconds and status.text.lower() not in exclusion_list:
            api.DestroyStatus(status.id)
    return


def main():

    """Deletes social media posts after they have been up for a certain number
    of days.
    """

    twitter_enabled = CONFIG['Twitter'].getboolean('enabled')

    if twitter_enabled:
        twitter_api = authenticate_twitter(CONFIG)
        print(('Authenticated for Twitter user ' +
               twitter_api.VerifyCredentials().screen_name),)

        exclude_words = CONFIG['General']['exclude key words'].split(",")
        for item in exclude_words:
            item.lower()

        print(('Deleting Twitter posts.'),)
        last_status_id = sys.maxsize
        status_set = twitter_api.GetUserTimeline(exclude_replies=False,
                                                 include_rts=True)
        while status_set:
            last_status_id = status_set[len(status_set) - 1].id
            delete_old_tweets(status_set, int(
                CONFIG['Twitter']['days']), twitter_api, exclude_words)
            status_set = twitter_api.GetUserTimeline(exclude_replies=False,
                                                     include_rts=True,
                                                     max_id=last_status_id - 1)

        print(('All posts older than ' + str(CONFIG['Twitter']['days']) +
               ' days have been deleted.'),)


if __name__ == "__main__":
    main()
