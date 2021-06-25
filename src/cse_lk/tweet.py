"""Tweet."""

from utils import twitter, timex

from cse_lk import daily_summary


def _tweet():
    daily_blurb_info = get_daily_blurb_info()

    ut = timex.get_unixtime()
    current_daily_summary = daily_summary.get_current_daily_summary(ut)
    if not current_daily_summary:
        return
    date = timex.format_time(ut, '%Y-%m-%d')

    current_daily_summary = list(reversed(current_daily_summary))
    rendered_highlight_lines = ['🟢 GAINERS']
    for datum in current_daily_summary[:5]:
        rendered_highlight_lines.append(
            '{symbol} {p_delta_price:+.1%}'.format(
                symbol=datum['symbol'],
                p_delta_price=datum['p_delta_price'],
            )
        )

    rendered_highlight_lines += ['', '🔴 LOSERS']
    for datum in current_daily_summary[-5:]:
        rendered_highlight_lines.append(
            '{symbol} {p_delta_price:+.1%}'.format(
                symbol=datum['symbol'],
                p_delta_price=datum['p_delta_price'],
            )
        )

    rendered_highlights = '\n'.join(rendered_highlight_lines)

    tweet_text = '''#Colombo Stock Exchange {date}

{rendered_highlights}

#SriLanka #lka #CSE @CSE_Media
    '''.format(
        date=date,
        rendered_highlights=rendered_highlights,
    )

    twtr = twitter.Twitter.from_args()
    twtr.tweet(
        tweet_text=tweet_text,
        update_user_profile=True,
    )


if __name__ == '__main__':
    _tweet()
