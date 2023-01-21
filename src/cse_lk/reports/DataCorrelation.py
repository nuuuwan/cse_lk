from functools import cached_property

from cse_lk.core.StockList import StockList
from cse_lk.reports.Data import Data


class DataCorrelation(Data):
    @cached_property
    def data(self):
        stock_list = StockList.load_from_remote()
        return stock_list.get_correlation_data_list()
    

if __name__ == '__main__':
    data_list = DataCorrelation().load()
    print(data_list[0])
