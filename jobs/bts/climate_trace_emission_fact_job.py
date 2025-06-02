from yaetos.etl_utils import ETL_Base, Commandliner
import pandas as pd
import numpy as np


class Job(ETL_Base):
    def transform(self, climate_trace):
        # Code in pandas so limited in output size.
        df = climate_trace
        df['Emissions_post'] = df['Emissions'].apply(map_emissions)
        df = df[['Id', 'Name', 'Emissions_post']]
        df = df.explode('Emissions_post')
        dict_df = df['Emissions_post'].apply(pd.Series)
        result_df = df.drop('Emissions_post', axis=1).join(dict_df)
        result_df = result_df.drop(0, axis=1)
        result_df.index.name = 'index'
        return result_df


def map_emissions(years_list):
    rows = []
    if years_list is None:
        print('WARNING: Cases to inspect')
        return []
    for years_dict in years_list:
        for year, year_emission_list in years_dict.items():
            if isinstance(year_emission_list, np.ndarray):
                for ii, year_emission_dict in enumerate(year_emission_list):
                    row = year_emission_dict
                    row['year'] = year
                    row['item'] = ii
                    rows.append(row)
            elif year_emission_list is not None:
                raise Exception(f'Should not get here, var type {type(year_emission_list)}, year_emission_list: {year_emission_list}')
    return rows


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata_bts_climate.yml'}
    Commandliner(Job, **args)
