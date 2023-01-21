from dataclasses import dataclass

from utils import Directory, Git, TimeFormat, TSVFile

from cse_lk.core.DailySummary import DailySummary
from cse_lk.core.Stock import Stock
from cse_lk.core.StockListBase import StockListBase
from cse_lk.core.StockListData import StockListData
from cse_lk.core.StockListStatistics import StockListStatistics


class StockList(StockListData, StockListStatistics):
    pass