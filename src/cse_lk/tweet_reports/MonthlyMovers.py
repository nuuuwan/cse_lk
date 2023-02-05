from utils import SECONDS_IN, Time, TimeFormat

from cse_lk import DailySummary
from cse_lk.tweet_reports.BaseTweetReport import BaseTweetReport


class MonthlyMovers(BaseTweetReport):
    def __init__(self, mode):
        self.mode = mode

    @staticmethod
    def get_p_monthly(ds_list):
        ds_end = ds_list[-1]
        ut_end = ds_end.ut
        price_last_traded_end = ds_end.price_last_traded
        for ds in ds_list:
            ut = ds.ut
            dut = ut_end - ut
            if dut <= SECONDS_IN.WEEK * 4:
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
            p_monthly = MonthlyMovers.get_p_monthly(ds_list)
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
        MAX_INNER_LEN = 180
        for symbol, p_monthly in monthly_movers:
            line = f'{p_monthly:+.0%} {symbol}'
            inner += '\n' + line
            if len(inner) > MAX_INNER_LEN:
                break

        return f'''TOP 28-days {self.label} (as of {self.date})
{inner}
        '''
