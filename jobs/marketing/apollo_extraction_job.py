from yaetos.etl_utils import ETL_Base, Commandliner
from yaetos.env_dispatchers import Cred_Ops_Dispatcher
import pandas as pd
import requests
import time


class Job(ETL_Base):
    def transform(self, companies):
        creds = Cred_Ops_Dispatcher().retrieve_secrets(self.jargs.storage, aws_creds='yaetos/connections', local_creds=self.jargs.connection_file)
        token = creds.get(self.jargs.api_inputs['creds'], 'token')
        headers = {
            'accept': "application/json",
            'Cache-Control': 'no-cache',
            }

        data = []
        key_out = ["employment_history", "organization"]
        for ii, row in list(companies.iterrows()):
            url = f"https://api.apollo.io/v1/mixed_people/search"
            body = {
                "api_key": token,
                "q_organization_domains": row["url"],
                "page": 1,
                "person_titles": ["cto", "ceo", "data"]
            }
            resp, data_blob = self.pull_1page(url, headers, body)
            if resp:
                rows_in = [{key : val for key, val in sub.items() if key not in key_out} for sub in data_blob["people"]]
                rows_out = []
                for item in rows_in:
                    item["company_url"] = row["url"]
                    item["company_name"] = row["name"]
                    rows_out.append(item)
                data += rows_out
            self.logger.info(f"Finished pulling all repos in {row['name']}, row {ii}")
            time.sleep(5)  # i.e. 5 sec between requests for rate limiting
        apollo = pd.DataFrame(data)
        return apollo


    def pull_1page(self, url, headers, body):
        try:
            resp = requests.request("POST", url, headers=headers, json=body)
            data = resp.json()
            if isinstance(data, dict) and 'people' in data.keys() and isinstance(data['people'], list):
                size = len(data['people'])  
            else:
                size = None
            self.logger.info(f"Pulled data from {url}, size {size}")
        except Exception as ex:
            resp = None
            data = None
            self.logger.info(f"Couldn't pull data from {url} with error: {ex}")
        return resp, data


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
