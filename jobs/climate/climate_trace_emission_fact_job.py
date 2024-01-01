from yaetos.etl_utils import ETL_Base, Commandliner
from yaetos.env_dispatchers import Cred_Ops_Dispatcher
import pandas as pd
import numpy as np
import requests
import time
import json


class Job(ETL_Base):
    def transform(self, climate_trace):
        # columns = climate_trace.columns
        # df = climate_trace.drop(['Owners', 'Confidence'], axis=1)
        # df = climate_trace[['Id', 'Name', 'Emissions']][:5]
        # df = climate_trace.drop(['Owners', 'Confidence', 'Emissions'], axis=1)
        # import ipdb; ipdb.set_trace()
        df = climate_trace[:5]
        df['Emissions_post'] = df['Emissions'].apply(map_emissions)
        df = df[['Id', 'Name', 'Emissions_post']]
        # columns.
        # df = climate_trace[[]]
        df = df.explode('Emissions_post')

        dict_df = df['Emissions_post'].apply(pd.Series)
        result_df = df.drop('Emissions_post', axis=1).join(dict_df)
        # rows = []
        # df = climate_trace
        return result_df

        # - emissions
        # - owner
        # - Confidence
        # - Centroid

def map_emissions(years_list):
    # cellblocks = cell.keys()
    rows = []
    # for cellblock in cellblocks:
    # year_list = cell.keys()
    for years_dict in years_list:
        # year = year_dict.keys()[0]
        # keys = list(years_dict.keys())
        # year = keys[0]
        # print('----', year_dict)
        # print('----#', keys, year)
        # assert len(keys) == 1 # double check
        for year, year_emission_list in years_dict.items():
            # year = years_dict[]
            # year_emission_list = year_dict[year]
            # print('----##', year_emission_list)
            if isinstance(year_emission_list, np.ndarray):
                for ii, year_emission_dict in enumerate(year_emission_list):
                    row = year_emission_dict
                    row['year'] = year
                    row['item'] = ii
                    rows.append(row)
            elif year_emission_list is not None:
                print('Should not get here', type(year_emission_list), year_emission_list)
                # raise('Should not get here')
    return rows

if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
