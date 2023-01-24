"""Scrape."""
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import (TIME_FORMAT_DATE_ID, WWW, String, Time, TimeFormat, TSVFile,
                   get_date_id)

from cse_lk import _constants
from cse_lk._utils import log


def _scrape_html():
    """Run."""
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(_constants.URL_DAILY_SUMMARY)

    browser.find_element(
        "xpath",
        "//select[@name='DataTables_Table_0_length']/option[text()='All']",
    ).click()

    html = browser.page_source
    browser.quit()
    return html


def _parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    span_updated_time = soup.find('span', class_='updated-time')
    unixtime = (
        TimeFormat('MARKET STATISTICS AS OF %b %d, %Y, %I:%M:%S %p')
        .parse(span_updated_time.text.strip())
        .ut
    )

    date_id = TIME_FORMAT_DATE_ID.stringify(Time(unixtime))

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
        ] = list(
            map(
                lambda td_cell: td_cell.text.strip(),
                tr_company_row,
            )
        )

        daily_summary.append(
            {
                'name': name,
                'symbol': symbol,
                'share_volume': String(share_volume).int,
                'trade_volume': String(trade_volume).int,
                'price_previous_close': String(price_previous_close).float,
                'price_open': String(price_open).float,
                'price_high': String(price_high).float,
                'price_low': String(price_low).float,
                'price_last_traded': String(price_last_traded).float,
                'delta_price': String(delta_price).float,
                'delta_price_p': String(delta_price_p).float,
            }
        )
    daily_summary_file_name = f'/tmp/cse_lk.daily_summary.{date_id}.tsv'
    TSVFile(daily_summary_file_name).write(daily_summary)
    log.info(
        f'Parsed { len(daily_summary) } companies'
        + f' and saved to {daily_summary_file_name}',
    )
    return daily_summary


def dump_daily_summary():
    """Dump daily summary."""
    html = _scrape_html()
    log.info(
        f'Scraped { len(html) / 1000 } KB from {_constants.URL_DAILY_SUMMARY}',
    )
    return _parse_html(html)


def get_current_daily_summary(ut):
    """Get daily summary."""
    date_id = get_date_id()
    url = os.path.join(
        'https://raw.githubusercontent.com',
        'nuuuwan/cse_lk/data',
        'cse_lk.daily_summary.{date_id}.tsv'.format(date_id=date_id),
    )
    if not WWW(url).exists:
        log.warn(f'No data for {date_id}')
        return None

    current_daily_summary = WWW(url).readTSV()

    def _extend(row):
        price_previous_close = String(row['price_previous_close']).float
        price_last_traded = String(row['price_last_traded']).float
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
