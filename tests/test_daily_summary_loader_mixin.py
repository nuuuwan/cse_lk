from unittest import TestCase, skip

from cse_lk import DailySummary


class TestDailySummaryLoaderMixin(TestCase):
    def test_list_from_date_id(self):
        daily_summary_list = DailySummary.list_from_date_id('20230203')
        self.assertEqual(len(daily_summary_list), 252)

    @skip('len becomes out of date')
    def test_list_all(self):
        daily_summary_list = DailySummary.list_all()
        self.assertEqual(len(daily_summary_list), 72_485)

    @skip('len becomes out of date')
    def test_list_from_symbol(self):
        daily_summary_list = DailySummary.list_from_symbol('ABAN.N0000')
        self.assertEqual(len(daily_summary_list), 234)
