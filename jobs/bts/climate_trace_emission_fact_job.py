from yaetos.etl_utils import ETL_Base, Commandliner
import pandas as pd
import numpy as np


class Job(ETL_Base):
    def transform(self, climate_trace):
        # Code in pandas so limited in output size.
        df = climate_trace
        df['Emissions'] = df['EmissionsSummary'].apply(map_emissions)
        df = df[['Id', 'Name', 'Emissions']]
        return df


def map_emissions(cell_list):
    if cell_list is None:
        print('WARNING: Cases to inspect')
        return []
    out = cell_list[0]['EmissionsQuantity']
    return out


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
