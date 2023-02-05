from utils import Tweet, Twitter


class BaseTweetReport:
    @property
    def tweet_text_custom(self):
        raise NotImplementedError

    @property
    def tweet_text(self):
        return f'''{self.tweet_text_custom}
#CSE #SriLanka #LKA @CSE_Media'''

    @property
    def tweet(self):
        return Tweet(
            text=self.tweet_text,
        )

    def send(self):
        Twitter.from_args().send(self.tweet)

    def send_test(self):
        Twitter.from_environ_vars().send(self.tweet)
