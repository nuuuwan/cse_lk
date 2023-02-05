from functools import cached_property

from utils import SECONDS_IN, Time, TimeFormat

from cse_lk import DailySummary, TwitterNames
from cse_lk.tweet_reports.BaseTweetReport import BaseTweetReport


class MonthlyMovers(BaseTweetReport):
    TOLERANCE = SECONDS_IN.WEEK

    def __init__(self, mode, window_weeks):
        self.mode = mode
        self.window_weeks = window_weeks

    @property
    def min_dut(self):
        return self.max_dut - SECONDS_IN.WEEK

    @property
    def max_dut(self):
        return SECONDS_IN.WEEK * (self.window_weeks)

    @cached_property
    def ut(self):
        return Time().ut

    def get_p_monthly(self, ds_list):
        ds_end = ds_list[-1]
        ut_end = ds_end.ut
        dut_current = self.ut - ut_end
        if dut_current > MonthlyMovers.TOLERANCE:
            return None

        price_last_traded_end = ds_end.price_last_traded
        for ds in ds_list:
            ut = ds.ut
            dut = ut_end - ut
            if self.min_dut <= dut <= self.max_dut:
                price_last_traded = ds.price_last_traded
                p_monthly = (
                    price_last_traded_end - price_last_traded
                ) / price_last_traded
                return p_monthly
        return None

    @property
    def monthly_movers(self):
        idx_all = DailySummary.idx_all()
        monthly_movers = []
        for symbol, ds_list in idx_all.items():
            p_monthly = self.get_p_monthly(ds_list)
            if p_monthly is not None:
                monthly_movers.append([symbol, p_monthly])
        return list(sorted(monthly_movers, key=lambda x: x[1], reverse=True))

    @property
    def monthly_gainers(self):
        return [
            [symbol, p_monthly]
            for symbol, p_monthly in self.monthly_movers
            if p_monthly is not None and p_monthly > 0
        ]

    @property
    def monthly_losers(self):
        return list(
            reversed(
                [
                    [symbol, p_monthly]
                    for symbol, p_monthly in self.monthly_movers
                    if p_monthly is not None and p_monthly < 0
                ]
            )
        )

    @property
    def label(self):
        return 'GAINERS' if self.mode != 'losers' else 'LOSERS'

    @property
    def emoji(self):
        return '🟢' if self.mode != 'losers' else '🔴'

    @property
    def date(self):
        idx_all = DailySummary.idx_all()
        ut = max([ds_list[-1].ut for ds_list in idx_all.values()])
        return TimeFormat('%Y-%m-%d').stringify(Time(ut))

    @property
    def monthly_movers_from_mode(self):
        return (
            self.monthly_gainers
            if self.mode != 'losers'
            else self.monthly_losers
        )

    @property
    def tweet_text_custom(self):
        monthly_movers = self.monthly_movers_from_mode
        inner = ''
        MAX_INNER_LEN = 170
        n_displayed = 0
        for symbol, p_monthly in monthly_movers:
            display_name = TwitterNames.get(symbol)
            line = f'{self.emoji} {p_monthly:+.0%} {display_name}'
            if len(inner + line) > MAX_INNER_LEN:
                break
            inner += '\n' + line
            if n_displayed % 5 == 4:
                inner += '\n'
            n_displayed += 1

        return f'''TOP {self.window_weeks}-week {self.label} (as of {self.date})
{inner}'''
