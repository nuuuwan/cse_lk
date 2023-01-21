from functools import cached_property

from cse_lk.core.StockList import StockList
from cse_lk.reports.Data import Data


class DataCorrelation(Data):
    def clean(self, x):
        x['correlation'] = float(x['correlation'])
        return x

    @cached_property
    def data(self):
        stock_list = StockList.load_from_remote()
        return stock_list.get_correlation_data_list()


def format_name(x):
    x = x.replace('PLC', '')
    x = x.strip().title()
    x = x.replace('C I C', 'CIC')
    x = x.replace('L O L C', 'LOLC')
    return x


class AnalyzeCorrelation:
    def do(self):
        data_list = DataCorrelation().load()
        high_correlation_pairs = []
        for data in data_list:
            if data['correlation'] < -LIMIT:
                if data['stock_i_name'][:4] == data['stock_j_name'][:4]:
                    print(data)
                    continue
                high_correlation_pairs.append(
                    [data['stock_i_name'], data['stock_j_name']]
                )

        for i, pair in enumerate(high_correlation_pairs):
            print(f'{i + 1}) {format_name(pair[0])} & {format_name(pair[1])}')


if __name__ == '__main__':

    AnalyzeCorrelation().do()
