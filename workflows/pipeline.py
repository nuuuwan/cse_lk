from cse_lk import CSEWebsiteDailySummary, MonthlyMovers

if __name__ == '__main__':
    CSEWebsiteDailySummary().parse_and_save()
    MonthlyMovers('gainers').send()
    MonthlyMovers('losers').send()
