from unittest import TestCase, skip

from cse_lk import MonthlyMovers

TEST_REPORT = MonthlyMovers('gainers', 4)
TEST_REPORT_LOSERS = MonthlyMovers('losers', 4)


class TestMonthlyMovers(TestCase):
    @skip('values become out of date')
    def test_monthly_movers(self):
        self.assertEqual(
            TEST_REPORT.monthly_movers[0],
            ['SEYB.X0000', 0.37179487179487175],
        )

    @skip('values become out of date')
    def test_monthly_gainers(self):
        self.assertEqual(
            TEST_REPORT.monthly_gainers[0],
            ['SEYB.X0000', 0.37179487179487175],
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
        self.assertEqual(len(lines), 13)
        self.assertEqual(lines[0], 'TOP 4-week GAINERS (as of 2023-02-03)')
        self.assertEqual(lines[1], '')
        self.assertEqual(lines[2], '🟢 +37% @SeylanBank X')
        self.assertEqual(lines[3], '🟢 +36% @SampathBankPLC')
        self.assertEqual(lines[4], '🟢 +35% #ColomboCityHoldings')

        self.assertEqual(lines[-2], 'data: www.cse.lk')
        self.assertEqual(lines[-1], '#CSE #SriLanka #LKA @CSE_Media')

    # @skip('needs twitter API keys')
    def test_send(self):
        TEST_REPORT.send_test()
        TEST_REPORT_LOSERS.send_test()
