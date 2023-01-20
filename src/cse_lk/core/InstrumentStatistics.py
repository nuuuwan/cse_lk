import statistics


class InstrumentStatistics:
    @property
    def price_list(self):
        return [d.price_last_traded for d in self.daily_summary_list]

    @property
    def price_list_latest(self):
        N_LATEST = 90
        return self.price_list[-N_LATEST:]

    @property
    def mean(self):
        return statistics.mean(self.price_list_latest)

    @property
    def stdev(self):
        return statistics.stdev(self.price_list_latest)
