import os

from utils import WWW

from cse_lk.core.CommonMixin import CommonMixin


class DailySummaryLoaderMixin(CommonMixin):
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
