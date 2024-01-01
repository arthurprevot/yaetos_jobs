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
        return df

    def get_assets(self, countries=None, limit=None, offset=None):
        url = "https://api.climatetrace.org/v4/assets"
        args = '?'
        args += f'countries={countries}&' if countries else ''
        # args += 'sectors=waste&'
        # args += 'sectors=cropland-fires&'
        # args += 'subsectors=aluminum&'
        # args += 'year=2021&'
        args += f'limit={limit}&' if limit else ''
        args += f'offset={offset}&' if offset else ''
        url += args
        # self.logger.info(f"Pulling all assets row {url}")
        # response = requests.get(url)
        # data = response.json()
        try:
            resp = requests.get(url)
            data = resp.json()
            assets = data['assets']

            if isinstance(data, dict) and 'assets' in data.keys() and isinstance(data['assets'], list):
                size = len(data['assets'])
            else:
                size = None
            self.logger.info(f"Pulled data from {url}, size {size}")
        except Exception as ex:
            resp = None
            data = None
            assets = []
            self.logger.info(f"Couldn't pull data from {url} with error: {ex}")

        rows = []
        for asset in assets:
            # fields = asset.keys()
            row = {key: asset[key] for key in asset.keys()}
            rows.append(row)

        return rows
        # return assets

    # def pull_1page(self, url, headers, body):
    #     try:
    #         resp = requests.request("POST", url, headers=headers, json=body)
    #         data = resp.json()
    #         if isinstance(data, dict) and 'people' in data.keys() and isinstance(data['people'], list):
    #             size = len(data['people'])
    #         else:
    #             size = None
    #         self.logger.info(f"Pulled data from {url}, size {size}")
    #     except Exception as ex:
    #         resp = None
    #         data = None
    #         self.logger.info(f"Couldn't pull data from {url} with error: {ex}")
    #     return resp, data


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
