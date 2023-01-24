from dataclasses import dataclass
from functools import cached_property


@dataclass
class StockBase:
    name: str
    symbol: str
    daily_summary_list: list

    @property
    def latest_daily_summary(self):
        return self.daily_summary_list[-1]

    @cached_property
    def name_short(self):
        name_short = self.name
        name_short = name_short.replace('PLC', '')
        name_short = name_short.strip()
        return name_short.title()


    @cached_property
    def symbol_short(self):
        symbol_short = self.symbol
        symbol_short = symbol_short.split('.')[0]
        return symbol_short
