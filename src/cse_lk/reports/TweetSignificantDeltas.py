from cse_lk.core.StockList import StockList
from cse_lk.reports.Tweet import Tweet

MAX_INSTRUMENTS = 8
MAX_CHARS_INNER_LINES = 150


class TweetSignificantDeltas(Tweet):
    @property
    def body_lines(self):
        stock_list = StockList.load_from_remote()
        date = stock_list[0].latest_daily_summary.date

        significant_stock_list = sorted(
            [stock for stock in stock_list],
            key=lambda x: -abs(x.latest_p_p_delta_price - 0.5),
        )

        inner_lines = ['']
        for stock in significant_stock_list:

            if len('\n'.join(inner_lines)) > MAX_CHARS_INNER_LINES:
                break

            line = ' '.join(
                [
                    f'{stock.latest_p_p_delta_price_icon}',
                    f'{stock.latest_p_p_delta_price_human}',
                    f'{stock.latest_p_delta_price:+.1%}',
                    stock.symbol_short,
                ]
            )
            inner_lines.append(line)

        inner_lines += ['', f'({date} EOT)']
        return inner_lines


if __name__ == '__main__':
    TweetSignificantDeltas().tweet()
