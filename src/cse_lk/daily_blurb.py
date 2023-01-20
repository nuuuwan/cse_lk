"""Scrape."""
import time

from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import JSONFile, Time, cache, get_date_id

from cse_lk import _constants
from cse_lk._utils import log


@cache(_constants.CACHE_NAME, _constants.CACHE_TIMEOUT)
def _scrape():
    """Run."""
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(_constants.URL_DAILY_BLURB)

    browser.set_window_size(1500, 1500)
    browser.execute_script('window.scrollTo(0, 500)')

    time.sleep(4)
    ss_image_1day_file = '/tmp/tmp.cse_lk.blurb.1day.ss.png'
    browser.save_screenshot(ss_image_1day_file)
    log.info('Saved ss to %s', ss_image_1day_file)

    browser.find_element(
        "xpath", "//select[@id='aspiDateRange']/option[text()='One year']"
    ).click()
    browser.find_element(
        "xpath", "//select[@id='snpDateRange']/option[text()='One year']"
    ).click()

    time.sleep(4)
    ss_image_1year_file = '/tmp/tmp.cse_lk.blurb.1year.ss.png'
    browser.save_screenshot(ss_image_1year_file)
    log.info('Saved ss to %s', ss_image_1year_file)

    html = browser.page_source
    browser.quit()
    return html, ss_image_1day_file, ss_image_1year_file


def _parse(html, ss_image_1day_file, ss_image_1year_file):
    soup = BeautifulSoup(html, 'html.parser')

    def _parse_float(x):
        x = x.replace(',', '')
        x = x.replace('%', '')
        return (float)(x)

    def _parse_index(index_name):
        div = soup.find('div', class_='quick-chart-content %s' % index_name)

        value = _parse_float(div.find('p', class_='change-amount').text)
        change = _parse_float(div.find('h3', class_='volume').text)
        p_change = _parse_float(div.find('p', class_='change-percent').text)

        return {
            'value': value,
            'change': change,
            'p_change': p_change / 100.0,
        }

    index_summary = {
        'aspi': _parse_index('aspi'),
        'snp': _parse_index('snp'),
    }

    im = Image.open(ss_image_1day_file)
    left, top = 175, 845
    width, height = 550, 395
    cropped_im1 = im.crop((left, top, left + width, top + height))
    cropped_im1 = cropped_im1.resize((800, 450))
    aspi_1day_image_file = '/tmp/tmp.cse_lk.aspi.1day.png'
    cropped_im1.save(aspi_1day_image_file)
    log.info('Saved cropped ss to %s', aspi_1day_image_file)

    left, top = 760, 845
    cropped_im2 = im.crop((left, top, left + width, top + height))
    cropped_im2 = cropped_im2.resize((800, 450))
    snp_1day_image_file = '/tmp/tmp.cse_lk.snp.1day.png'
    cropped_im2.save(snp_1day_image_file)
    log.info('Saved cropped ss to %s', snp_1day_image_file)

    im = Image.open(ss_image_1year_file)
    left, top = 175, 845
    width, height = 550, 395
    cropped_im1 = im.crop((left, top, left + width, top + height))
    cropped_im1 = cropped_im1.resize((800, 450))
    aspi_1year_image_file = '/tmp/tmp.cse_lk.aspi.1year.png'
    cropped_im1.save(aspi_1year_image_file)
    log.info('Saved cropped ss to %s', aspi_1year_image_file)

    left, top = 760, 845
    cropped_im2 = im.crop((left, top, left + width, top + height))
    cropped_im2 = cropped_im2.resize((800, 450))
    snp_1year_image_file = '/tmp/tmp.cse_lk.snp.1year.png'
    cropped_im2.save(snp_1year_image_file)
    log.info('Saved cropped ss to %s', snp_1year_image_file)

    return {
        'index_summary': index_summary,
        'image_files': [
            aspi_1day_image_file,
            snp_1day_image_file,
            aspi_1year_image_file,
            snp_1year_image_file,
        ],
    }


def get_daily_blurb_info():
    """Get daily blurb info."""
    html, ss_image_1day_file, ss_image_1year_file = _scrape()
    return _parse(html, ss_image_1day_file, ss_image_1year_file)


def dump_daily_blurb():
    Time().ut
    date_id = get_date_id()

    html, ss_image_1day_file, ss_image_1year_file = _scrape()
    _daily_blurb = _parse(html, ss_image_1day_file, ss_image_1year_file)
    index_summary = _daily_blurb['index_summary']
    daily_blurb_file_name = '/tmp/cse_lk.daily_blurb.%s.json' % date_id
    JSONFile(daily_blurb_file_name).write(index_summary)
    log.info(
        'Wrote daily blurb to %s',
        daily_blurb_file_name,
    )
