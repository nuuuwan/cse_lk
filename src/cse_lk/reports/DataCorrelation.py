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
    x = x.replace(' - ', '-')
    return x


class AnalyzeCorrelation:
    def do(self):
        data_list = DataCorrelation().load()
        high_correlation_pairs = []
        i = 0
        for data in sorted(
            data_list, key=lambda x: x['correlation'], reverse=False
        ):
            if data['stock_i_name'][:4] == data['stock_j_name'][:4]:
                continue

            high_correlation_pairs.append(
                [
                    data['stock_i_name'],
                    data['stock_j_name'],
                    data['correlation'],
                ]
            )

            correlation = data['correlation']
            print(
                ' '.join(
                    [
                        ' ',
                        str(i + 1) + ')',
                        format_name(data['stock_i_name']),
                        '&',
                        format_name(data['stock_j_name']),
                        f'({correlation:.2f})',
                    ]
                )
            )
            i += 1
            if i >= 20:
                break


if __name__ == '__main__':

    AnalyzeCorrelation().do()
