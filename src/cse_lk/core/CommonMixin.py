class CommonMixin:
    @staticmethod
    def get_daily_summary_list_path(date_id):
        return f'/tmp/cse_lk.daily_summary.{date_id}.tsv'
