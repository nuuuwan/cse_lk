from dataclasses import dataclass

from utils import String, Time, TimeFormat


@dataclass
class DailySummary:
    ut: int
    symbol: str
    share_volume: int
    trade_volume: int
    price_previous_close: float
    price_open: float
    price_high: float
    price_low: float
    price_last_traded: float

    @property
    def date_str(self):
        return TimeFormat('%Y-%m-%d').stringify(Time(self.ut))

    @property
    def delta_price(self):
        return self.price_last_traded - self.price_previous_close

    @property
    def p_delta_price(self):
        return self.delta_price / max(1, self.price_previous_close)

    def get_p_p_delta_price(self, p_delta_price_list):
        n = len(p_delta_price_list)
        p_delta_price = self.p_delta_price
        i_more = None
        for i, p in enumerate(p_delta_price_list):
            if p_delta_price < p:
                i_more = i
                break

        i_equal_list = []
        for i, p in enumerate(p_delta_price_list):
            if p_delta_price == p:
                i_equal_list.append(i)

        if i_equal_list:
            n_equal_list = len(i_equal_list)
            if n_equal_list % 2 == 1:
                i_mid = i_equal_list[(n_equal_list - 1) // 2]
            else:
                i_mid = i_equal_list[n_equal_list // 2] - 0.5
            return i_mid / n

        if i_more:
            return i_more / n

        return 1.0

    @staticmethod
    def from_dict(ut: int, d: dict):
        return DailySummary(
            ut=ut,
            symbol=d['symbol'],
            share_volume=String(d['share_volume']).int,
            trade_volume=String(d['trade_volume']).int,
            price_previous_close=String(d['price_previous_close']).float,
            price_open=String(d['price_open']).float,
            price_high=String(d['price_high']).float,
            price_low=String(d['price_low']).float,
            price_last_traded=String(d['price_last_traded']).float,
        )
