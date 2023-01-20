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
