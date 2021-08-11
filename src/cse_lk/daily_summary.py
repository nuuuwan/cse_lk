"""Scrape."""
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

from utils.cache import cache
from utils import dt, timex, tsv, www

from cse_lk import _constants
from cse_lk import _utils
from cse_lk._utils import log


@cache(_constants.CACHE_NAME, _constants.CACHE_TIMEOUT)
def _scrape_html():
    """Run."""
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(_constants.URL_DAILY_SUMMARY)

    browser.find_element_by_xpath(
        "//select[@name='DataTables_Table_0_length']/option[text()='All']"
    ).click()

    html = browser.page_source
    browser.quit()
    return html


def _parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    span_updated_time = soup.find('span', class_='updated-time')
    unixtime = timex.parse_time(
        span_updated_time.text.strip(),
        'MARKET STATISTICS AS OF %b %d, %Y, %I:%M:%S %p',
    )
    date_id = timex.format_time(unixtime, '%Y%m%d')

    daily_summary = []
    for i_row, tr_company_row in enumerate(soup.find_all('tr')):
        if i_row == 0:
            continue
        [
            name,
            symbol,
            share_volume,
            trade_volume,
            price_previous_close,
            price_open,
            price_high,
            price_low,
            price_last_traded,
            delta_price,
            delta_price_p,
        ] = list(map(
            lambda td_cell: td_cell.text.strip(),
            tr_company_row,
        ))

        daily_summary.append({
            'name': name,
            'symbol': symbol,
            'share_volume': _utils.parse_int(share_volume),
            'trade_volume': _utils.parse_int(trade_volume),
            'price_previous_close': dt.parse_float(price_previous_close),
            'price_open': dt.parse_float(price_open),
            'price_high': dt.parse_float(price_high),
            'price_low': dt.parse_float(price_low),
            'price_last_traded': dt.parse_float(price_last_traded),
            'delta_price': dt.parse_float(delta_price),
            'delta_price_p': dt.parse_float(delta_price_p),
        })
    daily_summary_file_name = '/tmp/cse_lk.daily_summary.%s.tsv' % date_id
    tsv.write(daily_summary_file_name, daily_summary)
    log.info(
        'Parsed %d companies and saved to %s',
        len(daily_summary),
        daily_summary_file_name,
    )
    return daily_summary


def dump_daily_summary():
    """Dump daily summary."""
    html = _scrape_html()
    log.info(
        'Scraped %dKB from %s',
        len(html) / 1000,
        _constants.URL_DAILY_SUMMARY,
    )
    return _parse_html(html)


def get_current_daily_summary(ut):
    """Get daily summary."""
    date_id = timex.format_time(ut, '%Y%m%d')
    url = os.path.join(
        'https://raw.githubusercontent.com',
        'nuuuwan/cse_lk/data',
        'cse_lk.daily_summary.{date_id}.tsv'.format(date_id=date_id),
    )
    if not www.exists(url):
        log.warn('No data for {date_id}'.format(date_id=date_id))
        return None

    current_daily_summary = www.read_tsv(url)

    def _extend(row):
        price_previous_close = dt.parse_float(row['price_previous_close'])
        price_last_traded = dt.parse_float(row['price_last_traded'])
        delta_price = price_last_traded - price_previous_close
        if not price_previous_close:
            row['p_delta_price'] = 0
        else:
            row['p_delta_price'] = delta_price / price_previous_close
        return row

    with_extended = list(map(_extend, current_daily_summary))
    sorted_extended = sorted(
        with_extended,
        key=lambda row: row['p_delta_price'],
    )

    return sorted_extended



if __name__ == '__main__':
    dump_daily_summary()
