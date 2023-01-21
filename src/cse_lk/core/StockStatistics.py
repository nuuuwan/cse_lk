import math
import statistics
from functools import cached_property

import numpy as np


class StockStatistics:
    @cached_property
    def price_list(self):
        return [d.price_last_traded for d in self.daily_summary_list]

    @cached_property
    def mean(self):
        return statistics.mean(self.price_list)

    @cached_property
    def stdev(self):
        return statistics.stdev(self.price_list)

    @cached_property
    def p_delta_price_list_unsorted(self):
        return [d.p_delta_price for d in self.daily_summary_list]

    @cached_property
    def p_delta_price_list(self):
        return sorted(self.p_delta_price_list_unsorted)

    @cached_property
    def latest_p_delta_price(self):
        return self.latest_daily_summary.p_delta_price

    @cached_property
    def latest_p_p_delta_price(self):
        return self.latest_daily_summary.get_p_p_delta_price(
            self.p_delta_price_list
        )

    @cached_property
    def latest_p_p_delta_price_human(self):
        latest_p_p_delta_price = self.latest_p_p_delta_price
        if latest_p_p_delta_price > 0.5:
            alpha = 1 - latest_p_p_delta_price
            sign = '🟢'
        else:
            alpha = latest_p_p_delta_price
            sign = '🔴'

        log_alpha = -math.log10(alpha)
        return (int)(log_alpha) * sign

    @cached_property
    def is_latest_significant(self):
        limit = 0.01
        return (
            self.latest_p_p_delta_price < limit
            or self.latest_p_p_delta_price > (1 - limit)
        )

    @cached_property
    def date_list(self):
        return [d.date for d in self.daily_summary_list]

    def get_common_date_list(self, other) -> list:
        return list(
            sorted(set(self.date_list).intersection(set(other.date_list)))
        )

    def get_p_delta_price_list_for_date_list(self, date_list) -> list:
        return [
            d.p_delta_price
            for d in self.daily_summary_list
            if d.date in date_list
        ]

    def get_correlation(self, other):
        MIN_COMMON_DATE_COUNT = 90
        common_date_list = self.get_common_date_list(other)
        if len(common_date_list) < MIN_COMMON_DATE_COUNT:
            return None
        return np.corrcoef(
            self.get_p_delta_price_list_for_date_list(common_date_list),
            other.get_p_delta_price_list_for_date_list(common_date_list),
        )[0, 1]
