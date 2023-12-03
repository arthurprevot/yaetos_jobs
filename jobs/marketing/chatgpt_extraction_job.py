from yaetos.etl_utils import ETL_Base, Commandliner
from yaetos.env_dispatchers import Cred_Ops_Dispatcher
import pandas as pd
import time
from openai import OpenAI


class Job(ETL_Base):
    def transform(self, companies):
        creds = Cred_Ops_Dispatcher().retrieve_secrets(self.jargs.storage, aws_creds='yaetos/connections', local_creds=self.jargs.connection_file)
        token = creds.get(self.jargs.api_inputs['creds'], 'token')
        client = OpenAI(api_key=token,)

        data = []
        for ii, row in list(companies.iterrows()):
            self.logger.info(f"Checking company {row['name']}")
            chat_prompt = self.generate_prompt(company=row["name"])

            # Doc: https://platform.openai.com/docs/api-reference/parameter-details?lang=python
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": chat_prompt},
                ]
            )

            chatout = response.choices[0].message.content if response else ''
            self.logger.info(f"Finished pulling chatgpt data, with prompt {chat_prompt}, and output: {chatout}")

            data_row = {
                'company_url': row["url"],
                'company_name': row["name"],
                "chatgpt_info": chatout,
            }
            data.append(data_row)
            time.sleep(0.3)  # wait in sec. openai rate limit unknown
        chatgpt = pd.DataFrame(data)
        return chatgpt

    @staticmethod
    def generate_prompt(company):
        return f"""
            Can you tell me what you know about the company called '{company}'.
            Put it in 300 characters.
            """


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
