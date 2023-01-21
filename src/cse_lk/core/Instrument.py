from utils import Directory, Git, TimeFormat, TSVFile

from cse_lk.core.DailySummary import DailySummary
from cse_lk.core.InstrumentBase import InstrumentBase
from cse_lk.core.InstrumentStatistics import InstrumentStatistics


class Instrument(InstrumentBase, InstrumentStatistics):
    @staticmethod
    def is_summary_file(child):
        return child.name.startswith('cse_lk.daily_summary.')

    @staticmethod
    def load_from_remote():
        git = Git('https://github.com/nuuuwan/cse_lk.git')
        git.clone('/tmp/cse_lk')
        git.checkout('data')

        symbol_to_daily_summary = {}
        symbol_to_name = {}

        for child in Directory('/tmp/cse_lk').children:
            if not Instrument.is_summary_file(child):
                continue
            date_str = child.name[21: 21 + 8]
            ut = TimeFormat('%Y%m%d').parse(date_str).ut
            data_list = TSVFile(child.path).read()

            for d in data_list:
                name = d['name']
                symbol = d['symbol']
                DailySummary.from_dict(ut, d)

                if symbol not in symbol_to_daily_summary:
                    symbol_to_daily_summary[symbol] = []
                symbol_to_daily_summary[symbol].append(
                    DailySummary.from_dict(ut, d)
                )

                symbol_to_name[symbol] = name

        instrument_list = []
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
            instrument = Instrument(
                symbol_to_name[symbol], symbol, daily_summary_list
            )
            instrument_list.append(instrument)

        return instrument_list


if __name__ == '__main__':
    instrument_list = Instrument.load_from_remote()
    for instrument in sorted(
        instrument_list, key=lambda x: x.latest_daily_summary.p_delta_price
    ):

        latest_p_p_delta_price = instrument.latest_p_p_delta_price
        latest_p_delta_price = instrument.latest_p_delta_price
        print(
            '\t'.join(
                [
                    f'{latest_p_delta_price:.1%}',
                    f'{ latest_p_p_delta_price:.1%}',
                    f'{instrument.latest_p_p_delta_price_human}',
                    instrument.symbol,
                    instrument.name,
                ]
            )
        )
