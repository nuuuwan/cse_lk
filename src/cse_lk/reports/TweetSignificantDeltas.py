from utils import twitter

from cse_lk.core.Stock import Stock

MAX_INSTRUMENTS = 8


class TweetSignificantDeltas:
    @property
    def header_lines(self):
        return [
            'SIGNIFICANT MOVES',
            '#Colombo Stock Exchange (#CSE)',
        ]

    @property
    def footer_lines(self):
        return [
            'Source: @CSE_Media #SriLanka #lka',
        ]

    @property
    def body_lines(self):
        stock_list = Stock.load_from_remote()
        date_str = stock_list[0].latest_daily_summary.date_str

        significant_stock_list = sorted(
            [stock for stock in stock_list if stock.is_latest_significant],
            key=lambda x: -x.latest_p_p_delta_price,
        )[:MAX_INSTRUMENTS]
        inner_lines = ['']
        for stock in significant_stock_list:
            line = ' '.join(
                [
                    f'{stock.latest_p_delta_price:+.1%}',
                    stock.symbol,
                    f'{stock.latest_p_p_delta_price_human}',
                ]
            )
            inner_lines.append(line)

        inner_lines += ['', f'({date_str} EOT)']
        return inner_lines

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


if __name__ == '__main__':
    TweetSignificantDeltas().tweet()
