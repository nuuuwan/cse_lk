from cse_lk.core.StockList import StockList
from cse_lk.reports.Tweet import Tweet

MAX_INSTRUMENTS = 8


class TweetSignificantDeltas(Tweet):
    @property
    def body_lines(self):
        stock_list = StockList.load_from_remote()
        date_str = stock_list[0].latest_daily_summary.date_str

        significant_stock_list = sorted(
            [stock for stock in stock_list if stock.is_latest_significant],
            key=lambda x: -x.latest_p_p_delta_price,
        )[:MAX_INSTRUMENTS]

        inner_lines = ['']
        for stock in significant_stock_list:
            line = ' '.join(
                [
                    f'{stock.latest_p_delta_price:+.1%}',
                    stock.symbol,
                    f'{stock.latest_p_p_delta_price_human}',
                ]
            )
            inner_lines.append(line)

        inner_lines += ['', f'({date_str} EOT)']
        return inner_lines


if __name__ == '__main__':
    TweetSignificantDeltas().tweet()
