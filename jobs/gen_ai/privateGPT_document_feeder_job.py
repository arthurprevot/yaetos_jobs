"""
PrivateGPT project available at https://github.com/imartinez/privateGPT 
Details about the privateGPT API: https://docs.privategpt.dev/
"""
from yaetos.etl_utils import ETL_Base, Commandliner
import requests
from yaetos.logger import setup_logging
logger = setup_logging('Job')


class Job(ETL_Base):
    def transform(self, listing):
        listing['in_gpt_store'] = listing.apply(lambda row: self.push_to_privategpt(doc=row['file_dir']+row['file_name']), axis=1)
        return listing

    @staticmethod
    def push_to_privategpt(doc):
        url = 'http://localhost:8001/v1/ingest'
        with open(doc, 'rb') as file:
            files = {'file': (file.name, file, 'application/pdf')}
            response = requests.post(url, files=files)
            if response.status_code == 200:
                logger.info(f"Transfered doc from {doc} to {url}, with output {response.text}")
                out = True
            else:
                logger.info(f"Couldn't transfer doc from {doc}. Output != 200, message: {response.text}")
                out = False
        return out


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
