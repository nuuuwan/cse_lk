from dataclasses import dataclass

from utils import String, Time, TimeFormat

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
