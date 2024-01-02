"""
More details about the data ingested at https://climatetrace.org/
Details about the API: https://api.climatetrace.org/v4/swagger/index.html
"""
from yaetos.etl_utils import ETL_Base, Commandliner
import pandas as pd
import requests


class Job(ETL_Base):
    def transform(self):
        # API requires knowing number of pages. TODO: implement way to get number of pages from API. Waiting for answer from climate trace.
        number_pages = 4
        all_rows = []
        for page in range(number_pages):
            rows = self.get_assets(countries=None, limit=None, offset=page)
            all_rows += rows
        df = pd.DataFrame(all_rows)
        # TODO: transition the code to spark to make it more scallable.
        return df

    def get_assets(self, countries=None, limit=None, offset=None):
        url = "https://api.climatetrace.org/v4/assets"
        args = '?'
        args += f'countries={countries}&' if countries else ''
        args += f'limit={limit}&' if limit else ''
        args += f'offset={offset}&' if offset else ''
        # Note: tested sectors, subsectors and year params but they don't seem to work
        url += args
        try:
            resp = requests.get(url)
            data = resp.json()
            assets = data['assets']
            size = len(assets) if isinstance(assets, list) else None
            self.logger.info(f"Pulled data from {url}, size {size}")
        except Exception as ex:
            resp = None
            data = None
            assets = []
            self.logger.info(f"Couldn't pull data from {url} with error: {ex}")

        return [asset | {'page': offset} for asset in assets]


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
