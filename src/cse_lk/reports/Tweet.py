from utils import twitter

MAX_INSTRUMENTS = 8


class Tweet:
    @property
    def header_lines(self):
        return [
            '#Colombo Stock Exchange (#CSE)',
        ]

    @property
    def footer_lines(self):
        return [
            '@CSE_Media #SriLanka #lka',
        ]

    @property
    def body_lines(self):
        raise NotImplementedError

    @property
    def tweet_lines(self):
        return self.header_lines + self.body_lines + self.footer_lines

    @property
    def tweet_text(self):
        return '\n'.join(self.tweet_lines)

    def tweet(self):
        twtr = twitter.Twitter.from_args()
        twtr.tweet(
            tweet_text=self.tweet_text,
        )
