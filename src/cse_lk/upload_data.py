"""Upload data."""

from cse_lk import daily_blurb, daily_summary

if __name__ == '__main__':
    daily_summary.dump_daily_summary()
    daily_blurb.dump_daily_blurb()
