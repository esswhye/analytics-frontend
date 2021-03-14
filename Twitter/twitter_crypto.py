from datetime import datetime, timezone

import streamlit as st
import tweepy
import constant
from Twitter.twitter_config import TwitterClient
from tweepy import Cursor

# https://stackoverflow.com/questions/30362651/getting-tweets-by-date-with-tweepy
# https://stackoverflow.com/questions/62738718/how-can-i-improve-my-error-handling-so-the-exception-stopiteration-in-tweepy-is
utc_datetime = datetime.now(tz=timezone.utc)
naive = utc_datetime.replace(tzinfo=None)
api = TwitterClient.api()

def crypto_tweets():
    st.subheader(
        f'Extract recent tweets with \'#\' sign and today\'s date {utc_datetime.strftime("%Y-%m-%d %H:%M:%S")} UTC')
    selectedUser = st.sidebar.selectbox("User ", constant.TWITTER_CRYPTOUSER_USERNAMES, index=0, key="cryto_user")
    tweetsCount = int(st.sidebar.text_input("Recent Tweets Count", value='10', max_chars=2, key="tweetsCount"))
    if selectedUser == "":
        return
    try:
        tweets = api.user_timeline(selectedUser, count=tweetsCount, exclude_replies=True)
        user = api.get_user(selectedUser)
        st.image(user.profile_image_url)
        st.write(user.name)
        st.write(f'https://twitter.com/{selectedUser}')
        for tweet in tweets:
            if (naive - tweet.created_at).days < 1:
                if '$' or '#' in tweet.text:
                    symbol = []
                    hashtag = []
                    words = tweet.text.split(' ')
                    for word in words:
                        if word.startswith('$') and word[1:].isalpha():
                            symbol.append(word[1:])
                        if word.startswith('#') and word[1:].isalpha():
                            hashtag.append(word[1:])
                    if (len(symbol) > 0 or len(hashtag) > 0):
                        st.write(f'.# {" ".join(hashtag)}')
                        st.write(f'.$ {" ".join(symbol)}')
                        st.write(tweet.text)
                        st.write(tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"))
                        st.write("-" * 50)
    except tweepy.TweepError as e:
        st.write("Tweepy Error: {}".format(e), "{} IS PRIVATE".format(e))
    pass


def crypto_graph():
    graph = {}
    for selectedUser in constant.TWITTER_CRYPTOUSER_USERNAMES:
        try:
            tweets = api.user_timeline(selectedUser, count=20, exclude_replies=True)
            for tweet in tweets:
                if (naive - tweet.created_at).days < 1:
                    if '$' or '#' in tweet.text:
                        words = tweet.text.split(' ')
                        for word in words:
                            if word.startswith('$') and word[1:].isalpha():
                                if checkKey(graph, word[1:]):
                                    graph[word[1:]] += 1
                                else:
                                    graph[word[1:]] = 1
                            if word.startswith('#') and word[1:].isalpha():
                                if checkKey(graph, word[1:]):
                                    graph[word[1:]] += 1
                                else:
                                    graph[word[1:]] = 1
        except tweepy.error.TweepError as e:
            continue
    st.write(graph)
    data = api.rate_limit_status()
    st.write(data['resources']['statuses']['/statuses/user_timeline'])
    return
    pass


def crypto():

    st.subheader('Crypto')
    crypto_category = st.sidebar.selectbox("Crypto Category ",["Tweets","Graph"], index=0, key="cryto_user")

    if crypto_category == "Tweets":
        crypto_tweets()

    if crypto_category == "Graph":
        crypto_graph()
    return


def friend_list(selectedUser):
    api = TwitterClient.api()
    user = api.get_user(selectedUser)
    friend_list = []
    #
    # for friend in Cursor(api.friends, screen_name=user).items():
    #     friend_list.append(friend)
    for friend in Cursor(api.friends, screen_name=user).items():
        print("APPENDING.. ")
        friend_list.append(friend)
    st.write(user.name)
    st.write(f'Friends: {len(friend_list)}')
    st.image(user.profile_image_url)
    return




def checkKey(dict, key):
    if key in dict:
        return True
    else:
        return False
