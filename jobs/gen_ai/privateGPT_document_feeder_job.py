"""
PrivateGPT project available at https://github.com/imartinez/privateGPT 
Details about the privateGPT API: https://docs.privategpt.dev/
"""
from yaetos.etl_utils import ETL_Base, Commandliner
import pandas as pd
import requests
from yaetos.logger import setup_logging
logger = setup_logging('Job')
# from io import BytesIO


class Job(ETL_Base):
    def transform(self, listing):
        # df = listing
        # row = listing.iloc[0]
        # doc = row['file_dir']+row['file_name']
        # self.push_to_privategpt(doc)
        # import ipdb; ipdb.set_trace()
        listing['in_gpt_store'] = listing.apply(lambda row: self.push_to_privategpt(doc=row['file_dir']+row['file_name']), axis=1)
        # docs 
        # for doc in docs:
        #     rows = self.push_doc_to_privategpt_store(doc)
        #     all_rows += rows
        # df = pd.DataFrame(all_rows)
        # TODO: transition the code to spark to make it more scallable.
        return listing

    @staticmethod
    def push_to_privategpt(doc):

        url = 'http://localhost:8001/v1/ingest'

        with open(doc, 'rb') as file:
            files = {'file': (file.name, file, 'application/pdf')}

            try:
                # response = requests.post(url, headers=headers, files=files)
                # response = requests.post(url, headers=headers, data=file_content)
                response = requests.post(url, files=files)
                if response.status_code == 200:
                    logger.info(f"Transfered doc from {doc} to {url}, with output {response.text}")
                    out = True
                else:
                    logger.info(f"Couldn't transfer doc from {doc}. Output != 200, message: {response.text}")
                    out = False
            except Exception as ex:
                logger.info(f"Couldn't transfer doc from {doc} with error: {ex}")
                out = False
        return out


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
