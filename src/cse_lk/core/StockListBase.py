from dataclasses import dataclass

from utils import Directory, Git, TimeFormat, TSVFile

from cse_lk.core.DailySummary import DailySummary
from cse_lk.core.Stock import Stock


@dataclass
class StockListBase:
    stock_list: list

    def __getitem__(self, index):
        return self.stock_list[index]
        
