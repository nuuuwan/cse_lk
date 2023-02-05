from unittest import TestCase, skip

from cse_lk import MonthlyMovers

TEST_REPORT = MonthlyMovers('gainers')
TEST_REPORT_LOSERS = MonthlyMovers('losers')


class TestMonthlyMovers(TestCase):
    @skip('values become out of date')
    def test_monthly_movers(self):
        self.assertEqual(
            TEST_REPORT.monthly_movers[0],
            ['CLC.N0000', 0.4412416851441241],
        )

    @skip('values become out of date')
    def test_monthly_gainers(self):
        self.assertEqual(
            TEST_REPORT.monthly_gainers[0],
            ['CLC.N0000', 0.4412416851441241],
        )

    @skip('values become out of date')
    def test_monthly_losers(self):
        self.assertEqual(
            TEST_REPORT.monthly_losers[0],
            ['JETS.N0000', -0.36363636363636365],
        )

    @skip('values become out of date')
    def test_tweet_text(self):
        tweet_text = TEST_REPORT.tweet_text
        lines = tweet_text.split('\n')
        self.assertEqual(len(lines), 17)
        self.assertEqual(lines[0], 'TOP 28-days GAINERS (as of 2023-02-03)')
        self.assertEqual(lines[1], '')
        self.assertEqual(lines[2], '+44% CLC.N0000')

    @skip('needs twitter API keys')
    def test_send(self):
        TEST_REPORT.send_test()
        TEST_REPORT_LOSERS.send_test()
