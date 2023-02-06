from cse_lk import CSEWebsiteDailySummary

if __name__ == '__main__':
    CSEWebsiteDailySummary().parse_and_save()
    # MonthlyMovers('gainers', 4).send()
    # MonthlyMovers('losers', 4).send()
    # MonthlyMovers('gainers', 12).send()
    # MonthlyMovers('losers', 12).send()
