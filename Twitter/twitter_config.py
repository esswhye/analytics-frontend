import tweepy
import config


class TwitterClient:
    __api = None

    @staticmethod
    def api():
        if TwitterClient.__api is None:
            print("initializing TwitterInit.Init")
            auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
            auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
            TwitterClient.__api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
        return TwitterClient.__api
