from dataclasses import dataclass

from utils import Log

log = Log('StockListStatistics')


@dataclass
class StockListStatistics:
    def get_correlation_data_list(self) -> dict:
        LIMIT = 0.75
        n = len(self)
        correlation_data_list = []
        for i in range(n - 1):
            for j in range(i + 1, n):
                correlation = self[i].get_correlation(self[j])
                if not correlation:
                    continue
                if abs(correlation) > LIMIT:
                    log.debug(
                        '\t'.join(
                            [
                                f'{correlation:.2f}',
                                self[i].name,
                                self[j].name,
                            ]
                        )
                    )

                correlation_data_list.append(
                    dict(
                        stock_i_symbol=self[i].symbol,
                        stock_i_name=self[i].name,
                        stock_j_symbol=self[j].symbol,
                        stock_j_name=self[j].name,
                        correlation=correlation,
                    )
                )

        return correlation_data_list
