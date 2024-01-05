from yaetos.etl_utils import ETL_Base, Commandliner
import pandas as pd
import numpy as np


class Job(ETL_Base):
    def transform(self, climate_trace):
        old_token = 'access_token=pk.eyJ1IjoiZWFydGhyaXNlIiwiYSI6ImNsN3NkMGkzdjBibWYzb2xhZndnNDc1d20ifQ.e4eN5Ee2g4G-zYcOgM-VQg'  # hardcoded in data probably by mistake.
        df = climate_trace.drop(['Emissions', 'Owners', 'Confidence'], axis=1)
        df['latitude'] = df['Centroid'].apply(lambda ce: ce['Geometry'][1])
        df['longitude'] = df['Centroid'].apply(lambda ce: ce['Geometry'][0])
        df['Thumbnail_post'] = df['Thumbnail'].apply(lambda ce: ce.replace(old_token, ''))
        df = df.drop(['Thumbnail'], axis=1)
        return df


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
