"""Tweet."""

from utils import twitter, timex

from cse_lk import daily_summary, daily_blurb


def _tweet():
    ut = timex.get_unixtime()
    date = timex.format_time(ut, '%Y-%m-%d')
    daily_blurb_info = daily_blurb.get_daily_blurb_info()
    index_summary = daily_blurb_info['index_summary']
    status_image_files = daily_blurb_info['image_files']

    def _format_change(x):
        if x >= 0:
            return '🟢 {x:+,}'.format(x=x)
        else:
            return '🔴 {x:+,}'.format(x=x)

    tweet_text = '''#Colombo Stock Exchange {date}

#ASPI: {aspi_value:,} {aspi_change}

@SPGlobalRatings #SL20: {snp_value:,} {snp_change}

#SriLanka #lka #CSE @CSE_Media
    '''.format(
        date=date,
        aspi_value=index_summary['aspi']['value'],
        snp_value=index_summary['snp']['value'],
        aspi_change=_format_change(index_summary['aspi']['change']),
        snp_change=_format_change(index_summary['snp']['change']),
    )
    print(tweet_text)
    print(len(tweet_text))
    # return

#     ut = timex.get_unixtime()
#     current_daily_summary = daily_summary.get_current_daily_summary(ut)
#     if not current_daily_summary:
#         return
#     date = timex.format_time(ut, '%Y-%m-%d')
#
#     current_daily_summary = list(reversed(current_daily_summary))
#     rendered_highlight_lines = ['🟢 GAINERS']
#     for datum in current_daily_summary[:5]:
#         rendered_highlight_lines.append(
#             '{symbol} {p_delta_price:+.1%}'.format(
#                 symbol=datum['symbol'],
#                 p_delta_price=datum['p_delta_price'],
#             )
#         )
#
#     rendered_highlight_lines += ['', '🔴 LOSERS']
#     for datum in current_daily_summary[-5:]:
#         rendered_highlight_lines.append(
#             '{symbol} {p_delta_price:+.1%}'.format(
#                 symbol=datum['symbol'],
#                 p_delta_price=datum['p_delta_price'],
#             )
#         )
#
#     rendered_highlights = '\n'.join(rendered_highlight_lines)
#
#     tweet_text = '''#Colombo Stock Exchange {date}
#
# {rendered_highlights}
#
# #SriLanka #lka #CSE @CSE_Media
#     '''.format(
#         date=date,
#         rendered_highlights=rendered_highlights,
#     )

    twtr = twitter.Twitter.from_args()
    twtr.tweet(
        tweet_text=tweet_text,
        status_image_files=status_image_files,
        update_user_profile=True,
    )


if __name__ == '__main__':
    _tweet()
