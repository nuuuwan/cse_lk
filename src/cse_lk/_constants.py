"""Constants."""
import os

URL_DAILY_BLURB = 'https://www.cse.lk'
URL_DAILY_SUMMARY = os.path.join(
    URL_DAILY_BLURB,
    'pages/trade-summary/trade-summary.component.html',
)


CACHE_NAME, CACHE_TIMEOUT = 'cse_lk', 3600
