from yaetos.etl_utils import ETL_Base, Commandliner
import pandas as pd
import requests
import time
from yaetos.env_dispatchers import Cred_Ops_Dispatcher


class Job(ETL_Base):
    def transform(self, startups):
        creds = Cred_Ops_Dispatcher().retrieve_secrets(self.jargs.storage, aws_creds='yaetos/connections', local_creds=self.jargs.connection_file)
        token = creds.get(self.jargs.api_inputs['creds'], 'token')
        headers = {
            'accept': "application/json",
            'Cache-Control': 'no-cache',
            }
        #import ipdb; ipdb.set_trace()
        data = []
        key_out = ["employment_history", "organization"]
        for ii, row in list(startups.iterrows()):
            #self.logger.info(f"About to pull email info for companie {row['url']}")
            url = f"https://api.apollo.io/v1/mixed_people/search"
            body = {
                "api_key": token,
                "q_organization_domains": row["url"],
                "page": 1,
                "person_titles": ["cto", "ceo", "data"]
            }
            resp, data_blob = self.pull_1page(url, headers, body)
            #import ipdb; ipdb.set_trace()
            if resp:
                data_rows = [{key : val for key, val in sub.items() if key not in key_out} for sub in data_blob["people"]]
                #data_rows = [**{"website": row["url"]}, **sub for sub in data_rows]
                data_rows2 = []
                for item in data_rows:
                    #item2 = {**{"website": row["url"]}, **item}
                    item["company_url"] = row["url"]
                    item["company_name"] = row["name"]
                    data_rows2.append(item)
                data += data_rows2
            self.logger.info(f"Finished pulling all repos in {row['name']}, row {ii}")
            time.sleep(5.*61 / 100.)  # i.e. 3.5 sec between requests. Apollo rate limit: 100 API requests per 5 minutes
            #time.sleep(1.001*60*60 / 100.)  # i.e. 36 sec between requests. Apollo rate limit: 100 times per hour
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
            #import ipdb; ipdb.set_trace()
            self.logger.info(f"Pulled data from {url}, size {size}")
        except Exception as ex:
            resp = None
            data = None
            self.logger.info(f"Couldn't pull data from {url} with error: {ex}")
        return resp, data


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
