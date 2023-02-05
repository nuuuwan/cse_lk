from unittest import TestCase

from cse_lk import DailySummary


class TestDailySummaryLoaderMixin(TestCase):
    def test_list_from_date_id(self):
        daily_summary_list = DailySummary.list_from_date_id('20230203')
        self.assertEqual(len(daily_summary_list), 252)
