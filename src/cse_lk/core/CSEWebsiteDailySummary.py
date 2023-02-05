import os
from functools import cached_property

from bs4 import BeautifulSoup
from utils import (TIME_FORMAT_DATE_ID, Browser, Log, String, Time, TimeFormat,
                   TSVFile)

from cse_lk.core.CommonMixin import CommonMixin
from cse_lk.core.DailySummary import DailySummary

log = Log('CSEWebsiteDailySummary')


class CSEWebsiteDailySummary(CommonMixin):
    URL = os.path.join(
        'https://www.cse.lk',
        'pages',
        'trade-summary',
        'trade-summary.component.html',
    )

    @property
    def html(self):
        browser = Browser()
        browser.open(self.URL)
        browser.find_element(
            "xpath",
            "//select[@name='DataTables_Table_0_length']/option[text()='All']",
        ).click()
        html = browser.source
        browser.quit()
        return html

    def _parse_row(self, tr_company_row, ut):
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
            _,  # delta_price,
            _,  # delta_price_p,
        ] = list(
            map(
                lambda td_cell: td_cell.text.strip(),
                tr_company_row,
            )
        )

        return DailySummary(
            ut=ut,
            symbol=symbol,
            name=name,
            share_volume=String(share_volume).int,
            trade_volume=String(trade_volume).int,
            price_previous_close=String(price_previous_close).float,
            price_open=String(price_open).float,
            price_high=String(price_high).float,
            price_low=String(price_low).float,
            price_last_traded=String(price_last_traded).float,
        )

    @cached_property
    def ut(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        span_updated_time = soup.find('span', class_='updated-time')
        return (
            TimeFormat('MARKET STATISTICS AS OF %b %d, %Y, %I:%M:%S %p')
            .parse(span_updated_time.text.strip())
            .ut
        )

    @cached_property
    def date_id(self):
        return TIME_FORMAT_DATE_ID.stringify(Time(self.ut))

    @cached_property
    def daily_summary_list_path(self):
        return CSEWebsiteDailySummary.get_daily_summary_list_path(
            self.date_id
        )

    @cached_property
    def daily_summary_list(self):
        ut = self.ut
        soup = BeautifulSoup(self.html, 'html.parser')
        daily_summary_list = []
        for i_row, tr_company_row in enumerate(soup.find_all('tr')):
            if i_row == 0:
                continue
            daily_summary = self._parse_row(tr_company_row, ut)
            daily_summary_list.append(daily_summary)

        return daily_summary_list

    def parse_and_save(self):
        daily_summary_list = self.daily_summary_list
        d_list = [d.to_dict() for d in daily_summary_list]

        TSVFile(self.daily_summary_list_path).write(d_list)
        n = len(daily_summary_list)
        log.info(f'Wrote {n} rows to {self.daily_summary_list_path}')
