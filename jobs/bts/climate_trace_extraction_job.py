"""
More details about the data ingested at https://climatetrace.org/
Details about the API: https://api.climatetrace.org/v6/swagger/index.html
"""
from yaetos.etl_utils import ETL_Base, Commandliner
import pandas as pd
import requests


class Job(ETL_Base):
    def transform(self):
        # Code in pandas so limited in output size.
        countries = None  # DON'T USE, pb with API outputing AssetCount=0
        continents = 'Oceania'
        years = ['2020', '2021', '2022', '2023', '2024', '2025']
        AssetCount, __ = self.get_assets_size(countries=countries, continents=continents)
        assets_per_page = 500
        number_pages = AssetCount // assets_per_page + 1
        self.logger.info(f"About to pull data for {AssetCount} assets, in {number_pages} api calls, with {assets_per_page} assets per call.")
        all_rows = []
        offset = 0
        for ii in range(number_pages):
            for year in years:
                rows = self.get_assets(countries=countries, continents=continents, year=year, limit=assets_per_page, offset=offset)
                offset += assets_per_page
                all_rows += rows
        df = pd.DataFrame(all_rows)
        return df

    def get_assets(self, countries=None, continents=None, year=None, limit=None, offset=None):
        url = "https://api.climatetrace.org/v6/assets"
        args = '?'
        args += f'countries={countries}&' if countries else ''
        args += f'continents={continents}&' if continents else ''
        args += f'year={year}&' if year else ''
        args += f'limit={limit}&' if limit else ''
        args += f'offset={offset}&' if offset else ''
        # Note: tested sectors, subsectors and year params but they didn't work
        url += args
        get_table = lambda data: data['assets']
        __, ___, assets = self.api_pull(url, get_table)
        assets = [asset | {'offset_batch': offset, 'year': year} for asset in assets]
        return assets

    def get_assets_size(self, countries=None, continents=None, limit=None):
        url = "https://api.climatetrace.org/v6/assets/emissions"
        args = '?'
        args += f'countries={countries}&' if countries else ''
        args += f'continents={continents}&' if continents else ''
        url += args
        dummy_size_fct = lambda data: None
        __, data, ___ = self.api_pull(url, dummy_size_fct)
        assert data is not None
        keys = list(data.keys())
        assert len(keys) == 1
        rows = data[keys[0]]
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
