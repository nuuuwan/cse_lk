from dataclasses import dataclass

from utils import String, Time, TimeFormat


def get_i_equal_list(value, value_list):
    return [x[0] for x in enumerate(value_list) if x[1] == value]


def get_i_more(value, value_list):
    more_list = [x[0] for x in enumerate(value_list) if x[1] > value]
    if not more_list:
        return None
    return more_list[0]


def get_p_mid(index_list, n):
    n_list = len(index_list)
    if n_list % 2 == 1:
        i_mid = index_list[(n_list - 1) // 2]
    else:
        i_mid = index_list[n_list // 2] - 0.5
    return i_mid / n


@dataclass
class DailySummary:
    ut: int
    symbol: str
    name: str
    share_volume: int
    trade_volume: int
    price_previous_close: float
    price_open: float
    price_high: float
    price_low: float
    price_last_traded: float

    @property
    def date(self):
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
        i_equal_list = get_i_equal_list(p_delta_price, p_delta_price_list)
        if i_equal_list:
            return get_p_mid(i_equal_list, n)
        i_more = get_i_more(p_delta_price, p_delta_price_list)
        if i_more:
            return i_more / n

        return 1.0

    @staticmethod
    def from_dict(ut: int, d: dict):
        return DailySummary(
            ut=ut,
            symbol=d['symbol'],
            name=d['name'],
            share_volume=String(d['share_volume']).int,
            trade_volume=String(d['trade_volume']).int,
            price_previous_close=String(d['price_previous_close']).float,
            price_open=String(d['price_open']).float,
            price_high=String(d['price_high']).float,
            price_low=String(d['price_low']).float,
            price_last_traded=String(d['price_last_traded']).float,
        )

    def to_dict(self):
        return {
            'ut': self.ut,
            'name': self.name,
            'symbol': self.symbol,
            'share_volume': self.share_volume,
            'trade_volume': self.trade_volume,
            'price_previous_close': self.price_previous_close,
            'price_open': self.price_open,
            'price_high': self.price_high,
            'price_low': self.price_low,
            'price_last_traded': self.price_last_traded,
        }
