
import tweepy
import textblob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re


# SIGN UP FOR TWITTER API BEFORE USING U CANT ANSWER THE NEXT 4 LINES!!!!!
api_key = ''
api_key_secret = '' 
access_token = ''
access_token_secret = ''

auth_handler = tweepy.OAuthHandler(consumer_key=api_key, consumer_secret=api_key_secret)
auth_handler.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler, wait_on_rate_limit=True)

crypto = 'near' #Insert Search Term Here

search = f'#{crypto} -filter:retweets'

tweet_cursor = tweepy.Cursor(api.search_tweets, q=search, lang='en', tweet_mode='extended').items(200)

tweets = [tweet.full_text for tweet in tweet_cursor]
print(tweets)
tweets_df = pd.DataFrame(tweets, columns=['tweets'])

for _, row in tweets_df.iterrows():
    row['tweets'] = re.sub('http\S+', '', row['tweets'])
    row['tweets'] = re.sub('#\S+', '', row['tweets'])
    row['tweets'] = re.sub('@\S+', '', row['tweets'])
    row['tweets'] = re.sub('\\n', '', row['tweets'])

tweets_df.to_csv("ONEONE.csv")
tweets_df['polarity'] = tweets_df['tweets'].map(lambda tweet: textblob.TextBlob(tweet).sentiment.polarity)
tweets_df['result'] = tweets_df['polarity'].map(lambda pol: '+' if pol > 0 else '-')

positive = tweets_df[tweets_df.values == '+'].count()['tweets']
negative = tweets_df[tweets_df.values == '-'].count()['tweets']

plt.bar([0, 1], [positive, negative], label=['Positive', 'Negative'], color=['green', 'red'])
plt.legend()
plt.show()

tweets_df.to_csv('twitterTweet.csv')
