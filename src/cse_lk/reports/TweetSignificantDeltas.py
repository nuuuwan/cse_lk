from utils import twitter

from cse_lk.core.Instrument import Instrument

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
        instrument_list = Instrument.load_from_remote()
        date_str = instrument_list[0].latest_daily_summary.date_str

        significant_instrument_list = sorted(
            [
                instrument
                for instrument in instrument_list
                if instrument.is_latest_significant
            ],
            key=lambda x: -x.latest_p_p_delta_price,
        )[:MAX_INSTRUMENTS]
        inner_lines = ['']
        for instrument in significant_instrument_list:
            line = ' '.join(
                [
                    f'{instrument.latest_p_delta_price:+.1%}',
                    instrument.symbol,
                    f'{instrument.latest_p_p_delta_price_human}',
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
