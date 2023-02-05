import os

from utils import WWW, Directory, Git, Log, TimeFormat, TSVFile

from cse_lk.core.CommonMixin import CommonMixin

log = Log('DailySummaryLoaderMixin')


class DailySummaryLoaderMixin(CommonMixin):
    GIT_REPO_URL = 'https://github.com/nuuuwan/cse_lk'
    DIR_URL = '/tmp/cse_lk'

    @staticmethod
    def get_url_for_date_id(date_id):
        return os.path.join(
            'https://raw.githubusercontent.com',
            'nuuuwan',
            'cse_lk',
            'data',
            f'cse_lk.daily_summary.{date_id}.tsv',
        )

    @classmethod
    def list_from_date_id(cls, date_id):
        d_list = WWW(
            DailySummaryLoaderMixin.get_url_for_date_id(date_id)
        ).readTSV()
        return [cls.from_dict(d) for d in d_list]

    @classmethod
    def list_all(cls):
        git = Git(DailySummaryLoaderMixin.GIT_REPO_URL)
        git.clone(DailySummaryLoaderMixin.DIR_URL, force=False)
        git.checkout('data')

        d_list = []
        for child in Directory(DailySummaryLoaderMixin.DIR_URL).children:
            if child.name.startswith(
                'cse_lk.daily_summary.'
            ) and child.name.endswith('.tsv'):
                log.debug(f'Reading file {child.name}')
                d_list_raw = TSVFile(child.path).read()
                # FIX: legacy time format missing ut
                ut = TimeFormat('%Y%m%d').parse(child.name[21:29]).ut
                d_list_raw = [d | {'ut': str(ut)} for d in d_list_raw]
                d_list += d_list_raw

        return [cls.from_dict(d) for d in d_list]

    @classmethod
    def list_from_symbol(cls, symbol):
        return [ds for ds in cls.list_all() if ds.symbol == symbol]
