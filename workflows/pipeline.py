from utils import Log
from cse_lk import CSEWebsiteDailySummary, MonthlyMovers
log = Log('cse_lk')

if __name__ == '__main__':
    CSEWebsiteDailySummary().parse_and_save()

    try:
        MonthlyMovers('gainers', 4).send()
        MonthlyMovers('losers', 4).send()
        MonthlyMovers('gainers', 12).send()
        MonthlyMovers('losers', 12).send()
    except BaseException as e:
        log.error(e)
