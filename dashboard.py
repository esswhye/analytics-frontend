import streamlit as st
import requests
import datetime

import tweepy

import config
import constant
from Twitter import twitter_stock
from Twitter.twitter_crypto import crypto


st.sidebar.title("Options")
option = st.sidebar.selectbox("Which Dashboard?", constant.LIST_DASHBOARD_NAMES)

st.title(option)

# https://www.tweepy.org/
if option == 'Twitter':
    twitterCategory = st.sidebar.selectbox("Select Category ", constant.TWITTER_CATEGORY)
    try:
        if twitterCategory == constant.TWITTER_CATEGORY[0]:
            crypto()
        if twitterCategory == constant.TWITTER_CATEGORY[1]:
            twitter_stock.stock()
    except tweepy.TweepError as e:
        st.write(e)

if option == 'WallStreetBets':
    st.subheader("WallStreetBets Dashboard")

if option == 'Chart':
    st.subheader("Chart Dashboard")

# https://stocktwits.com/
if option == 'Stocktwits':
    symbol = st.sidebar.text_input("Symbol", value='AAPL', max_chars=5)
    st.subheader("Stocktwits Dashboard")
    r = requests.get(f'https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json')
    data = r.json()
    stockTwitsRateRemaining = r.headers['X-RateLimit-Remaining']
    st.write(f'Remaining calls: {stockTwitsRateRemaining}')
    if data['response']['status'] == 200:
        for message in data['messages']:
            st.write(message['user']['username'])
            st.image(message['user']['avatar_url'])
            st.write(message['body'])
            created_at = datetime.datetime.strptime(message['created_at'], "%Y-%m-%dT%H:%M:%S%z")
            st.write(created_at)
            st.write("-" * 50)
    else:
        st.write(data)

if option == 'Pattern':
    st.subheader("Pattern Dashboard")
