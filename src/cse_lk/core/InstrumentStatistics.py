import math
import statistics


class InstrumentStatistics:
    @property
    def price_list(self):
        return [d.price_last_traded for d in self.daily_summary_list]

    @property
    def mean(self):
        return statistics.mean(self.price_list)

    @property
    def stdev(self):
        return statistics.stdev(self.price_list)

    @property
    def p_delta_price_list(self):
        return sorted([d.p_delta_price for d in self.daily_summary_list])

    @property
    def latest_p_delta_price(self):
        return self.latest_daily_summary.p_delta_price

    @property
    def latest_p_p_delta_price(self):
        return self.latest_daily_summary.get_p_p_delta_price(
            self.p_delta_price_list
        )

    @property
    def latest_p_p_delta_price_human(self):
        latest_p_p_delta_price = self.latest_p_p_delta_price
        if latest_p_p_delta_price > 0.5:
            alpha = (1 - latest_p_p_delta_price) * 2
            sign = '+'
        else:
            alpha = latest_p_p_delta_price * 2
            sign = '-'

        log_alpha = -math.log10(alpha)
        return (int)(log_alpha) * sign
