#!/usr/bin/env python
### David Chan, Nathan Saslavsky Kendall Weistroffer
### Sphero Twitter Bot
### April 1, 2016

### Setup Imports ###

import ConfigParser
import json
import re
import tweepy

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

### Manage API client connection information ###

config = ConfigParser.ConfigParser()
config.read('twitter.config')

consumer_key = config.get('apikey', 'key')
consumer_secret = config.get('apikey', 'secret')
access_token = config.get('token', 'token')
access_token_secret = config.get('token', 'secret')
stream_rule = config.get('app', 'rule')
account_screen_name = config.get('app', 'account_screen_name').lower() 
account_user_id = config.get('app', 'account_user_id')

### Perform authentication ###

auth = OAuthHandler(consumer_key, consumer_secret, secure=True)
auth.set_access_token(access_token, access_token_secret)
twitterApi = API(auth)

### Build handler for tweets ###

class ChangeColor(StreamListener):

    def on_data(self, data):
        print(data)
        tweet = json.loads(data.strip())
        
        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user',{}).get('id_str','') == account_user_id

        if retweeted is not None and not retweeted and not from_self:

            tweetId = tweet.get('id_str')
            screenName = tweet.get('user',{}).get('screen_name')
            tweetText = tweet.get('text')

            ### Extract colors from the recieved tweet ###

            color = re.search('[#][A-Fa-f0-9]{6}',tweetText).group()
            if color is not None:
                replyText = 'Just for '+ '@' + str(screenName) + ' I am changing color to ' + str(color)
                if len(replyText) > 140:
                    replyText = replyText[0:136] + '...'
                print('Tweet ID: ' + tweetId)
                print('From: ' + screenName)
                print('Tweet Text: ' + tweetText)
                print('Reply Text: ' + replyText)

                # Respond to the user
                twitterApi.update_status(status=replyText, in_reply_to_status_id=tweetId)

    def on_error(self, status):
        print(status)

### Construct tweet stream ###
if __name__ == '__main__':
    streamListener = ChangeColor()
    twitterStream = Stream(auth, streamListener)
    twitterStream.filter(track=['@DUSphero'])
