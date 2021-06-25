"""Tests for scrape."""
import unittest

from cse_lk import daily_summary


class TestScrape(unittest.TestCase):
    """Tests."""

    def test_scrape(self):
        """Test."""
        _daily_summary = daily_summary.dump_daily_summary()
        self.assertGreater(len(_daily_summary), 100)
        self.assertIn('name', _daily_summary[0])


if __name__ == '__main__':
    unittest.main()
