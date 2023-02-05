from utils import Directory, Git, TimeFormat, TSVFile

from cse_lk.core.DailySummary import DailySummary
from cse_lk.core.Stock import Stock
from cse_lk.core.StockListBase import StockListBase
from cse_lk.core.StockListStatistics import StockListStatistics


class StockList(StockListBase, StockListStatistics):
    @staticmethod
    def is_summary_file(child):
        return child.name.startswith('cse_lk.daily_summary.')

    @staticmethod
    def load_from_remote_helper():
        git = Git('https://github.com/nuuuwan/cse_lk.git')
        git.clone('/tmp/cse_lk')
        git.checkout('data')

        symbol_to_daily_summary = {}
        symbol_to_name = {}
        for child in Directory('/tmp/cse_lk').children:
            if not StockList.is_summary_file(child):
                continue
            ut = TimeFormat('%Y%m%d').parse(child.name[21: 21 + 8]).ut
            data_list = TSVFile(child.path).read()

            for d in data_list:
                symbol = d['symbol']
                DailySummary.from_dict(ut, d)

                if symbol not in symbol_to_daily_summary:
                    symbol_to_daily_summary[symbol] = []
                symbol_to_daily_summary[symbol].append(
                    DailySummary.from_dict(ut, d)
                )
                symbol_to_name[symbol] = d['name']

        return [symbol_to_daily_summary, symbol_to_name]

    @staticmethod
    def load_from_remote():
        [
            symbol_to_daily_summary,
            symbol_to_name,
        ] = StockList.load_from_remote_helper()
        stock_list = []
        for symbol, daily_summary_list in symbol_to_daily_summary.items():
            daily_summary_list = sorted(
                list(
                    filter(
                        lambda x: x.price_previous_close
                        and x.price_last_traded,
                        daily_summary_list,
                    )
                ),
                key=lambda x: x.ut,
            )
            stock = Stock(symbol_to_name[symbol], symbol, daily_summary_list)
            stock_list.append(stock)

        return StockList(stock_list)
