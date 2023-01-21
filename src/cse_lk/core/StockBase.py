from dataclasses import dataclass


@dataclass
class StockBase:
    name: str
    symbol: str
    daily_summary_list: list

    @property
    def latest_daily_summary(self):
        return self.daily_summary_list[-1]
