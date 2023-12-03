from yaetos.etl_utils import ETL_Base, Commandliner
from yaetos.env_dispatchers import Cred_Ops_Dispatcher
import pandas as pd
import numpy as np
import requests
import time
import openai


class Job(ETL_Base):
    def transform(self, companies):
        creds = Cred_Ops_Dispatcher().retrieve_secrets(self.jargs.storage, aws_creds='yaetos/connections', local_creds=self.jargs.connection_file)
        token = creds.get(self.jargs.api_inputs['creds'], 'token')
        openai.api_key = token

        data = []
        for ii, row in list(companies.iterrows()):
            #self.logger.info(f"About to pull email info for companie {row['url']}")
            self.logger.info(f"Checking company {row['name']}")
            #import ipdb; ipdb.set_trace()
            # if not (type(row["linkedin_url"]) == float and np.isnan(row["linkedin_url"])) :
            chat_prompt = self.generate_prompt(company=row["name"] )
            # print(chat_prompt)

            # Doc: https://platform.openai.com/docs/api-reference/parameter-details?lang=python
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt= chat_prompt,
                temperature=0.1,
            )
            self.logger.info(f"Finished pulling chatgpt data, with prompt {chat_prompt}, and output: {response['choices'][0]['text'] if response else ''}")
            # else:
            #     response = None

            #import ipdb; ipdb.set_trace()
            data_row = {
                'company_url': row["url"], 
                'company_name': row["name"],
                "similarity": response["choices"][0]["text"] if response else '',
            }
            data.append(data_row)
            time.sleep(0.3)  # wait in sec. openai rate limit unknown
        chatgpt = pd.DataFrame(data)
        return chatgpt

    @staticmethod
    def generate_prompt(company):
        return f"""
            Can you tell me what you know about the company called '{company}'.
            Put it in 1 sentence.
            """


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
