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

        countries = 'USA'
        countries = 'AND'
        AssetCount, Emissions = self.get_assets_size(countries=countries)

        # import ipdb; ipdb.set_trace()
        assets_per_page = 10
        number_pages = AssetCount // assets_per_page + 1
        self.logger.info(f"About to pull data for {AssetCount} assets, in {number_pages} api calls, with {assets_per_page} assets per call.")
        # import ipdb; ipdb.set_trace()
        all_rows = []
        offset = 0
        for page in range(number_pages):
            rows = self.get_assets(countries=countries, limit=assets_per_page, offset=offset)
            offset += assets_per_page
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
        get_table = lambda data: data['assets']
        __, ___, assets = self.api_pull(url, get_table)
        assets = [asset | {'offset_batch': offset} for asset in assets]
        return assets

    def get_assets_size(self, countries=None, limit=None):
        url = "https://api.climatetrace.org/v4/assets/emissions"
        args = '?'
        args += f'countries={countries}&' if countries else ''
        url += args
        get_size_fct = lambda data: None
        __, data, ___ = self.api_pull(url, get_size_fct)
        keys = list(data.keys())
        assert len(keys) == 1
        rows = data[keys[0]]
        # import ipdb; ipdb.set_trace()
        AssetCount = sum([item['AssetCount'] for item in rows])
        Emissions = sum([item['Emissions'] for item in rows])  # TODO: make sure it can be sumed.
        return AssetCount, Emissions


    def api_pull(self, url, get_size_fct):
        try:
            resp = requests.get(url)
            data = resp.json()
            rows = get_size_fct(data)
            size = len(rows) if isinstance(rows, list) else None
            self.logger.info(f"Pulled data from {url}, size {size}")
        except Exception as ex:
            resp = None
            data = None
            rows = []
            self.logger.info(f"Couldn't pull data from {url} with error: {ex}")
        return resp, data, rows


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
