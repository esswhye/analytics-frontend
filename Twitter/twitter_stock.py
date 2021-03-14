import streamlit as st
import config
from Twitter.twitter_config import TwitterClient
import constant


def stock():
    st.subheader('Stock')
    st.subheader('Extract recent tweets with \'$\' sign ')
    selectedUser = st.sidebar.selectbox("User ", constant.TWITTER_TRADER_USERNAMES, index= 0)
    if selectedUser == "":
        return
    tweetsCount = int(st.sidebar.text_input("Recent Tweets Count", value='20', max_chars=2, key="tweetsCount"))
    tweets = TwitterClient.api().user_timeline(selectedUser, count=tweetsCount, exclude_replies=True)
    user = TwitterClient.api().get_user(selectedUser)
    st.write(user.name)
    st.image(user.profile_image_url)
    for tweet in tweets:
        if '$' in tweet.text:
            words = tweet.text.split(' ')
            for word in words:
                if word.startswith('$') and word[1:].isalpha():
                    symbol = word[1:]
                    st.write('symbol')
                    st.write(tweet.text)
                    st.image(f'https://finviz.com/chart.ashx?t={symbol}')
                    st.write(tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"))
                    st.write("-" * 50)
    return
