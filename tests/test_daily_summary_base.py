from unittest import TestCase

from cse_lk import DailySummary

TEST_DAILY_SUMMARY = DailySummary(
    ut=1675571435,
    symbol='ABC',
    name='ABC Company',
    share_volume=100,
    trade_volume=1000,
    price_previous_close=10.0,
    price_open=9.0,
    price_high=11.0,
    price_low=9.0,
    price_last_traded=10.0,
)


class TestDailySummaryBase(TestCase):
    def test_date(self):
        self.assertEqual(
            TEST_DAILY_SUMMARY.date,
            '2023-02-05',
        )

    def test_delta_price(self):
        self.assertEqual(
            TEST_DAILY_SUMMARY.delta_price,
            0.0,
        )
