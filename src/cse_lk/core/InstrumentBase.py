from dataclasses import dataclass

from cse_lk.core.DailySummary import DailySummary


@dataclass
class InstrumentBase:
    name: str
    symbol: str
    daily_summary_list: list

    @property
    def latest_daily_summary(self):
        return self.daily_summary_list[-1]
