import os

from utils import JSONFile, String

from cse_lk.core.DailySummary import DailySummary

TWITTER_NAMES = JSONFile('src/cse_lk/core/TWITTER_NAMES.json').read()


class TwitterNames:
    @staticmethod
    def get(symbol):
        return TWITTER_NAMES.get(symbol, symbol)

    @staticmethod
    def analyze():
        daily_summary_list = DailySummary.list_all()
        n_display = 0
        printed_set = set()
        for ds in daily_summary_list:
            symbol = ds.symbol
            if symbol in TWITTER_NAMES:
                continue
            if symbol in printed_set:
                continue
            name = ds.name
            name = (
                name.replace('PLC', '')
                .replace('Limited', '')
                .replace('Company', '')
            )
            twitter_name = '#' + String(name).camel
            print(f"'{symbol}': '{twitter_name}',")
            printed_set.add(symbol)

            search_key = String(name).snake.replace('_', ' ').title()
            url = f'https://twitter.com/search?q={search_key}&src=typed_query'
            os.system(f'open -a firefox "{url}"')

            n_display += 1
            if n_display > 10:
                break


if __name__ == '__main__':
    TwitterNames.analyze()
