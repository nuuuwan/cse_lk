from unittest import TestCase, skip

from bs4 import BeautifulSoup
from utils import File

from cse_lk import CSEWebsiteDailySummary

TEST_CSEWDS_HTML_ONLY = CSEWebsiteDailySummary()


class CSEWebsiteDailySummaryMockHack(CSEWebsiteDailySummary):
    @property
    def html(self):
        return File('tests/test_cse_website_daily_summary.html').read()


TEST_CSEWDS_NOT_HTML = CSEWebsiteDailySummaryMockHack()
TEST_DAILY_SUMMARY_AS_DICT = {
    'ut': 1675407195.0,
    'name': 'ABANS ELECTRICALS PLC',
    'symbol': 'ABAN.N0000',
    'share_volume': 57,
    'trade_volume': 6,
    'price_previous_close': 160.25,
    'price_open': 161.0,
    'price_high': 161.0,
    'price_low': 160.0,
    'price_last_traded': 160.25,
}


class TestCSEWebsiteDailySummary(TestCase):
    @skip('slow')
    def test_html(self):
        html = TEST_CSEWDS_HTML_ONLY.html
        self.assertEqual(html[:20], '<html class=" eventl')

    def test_parse_row(self):
        soup = BeautifulSoup(TEST_CSEWDS_HTML_ONLY.html, 'html.parser')
        tr_company_row = soup.find_all('tr')[1]
        daily_summary = TEST_CSEWDS_NOT_HTML._parse_row(
            tr_company_row=tr_company_row, ut=1675407195.0
        )
        self.assertEqual(
            daily_summary.to_dict(),
            TEST_DAILY_SUMMARY_AS_DICT,
        )

    def test_daily_summary_list(self):
        daily_summary_list = TEST_CSEWDS_NOT_HTML.daily_summary_list
        self.assertEqual(len(daily_summary_list), 252)
        self.assertEqual(
            daily_summary_list[0].to_dict(),
            TEST_DAILY_SUMMARY_AS_DICT,
        )
