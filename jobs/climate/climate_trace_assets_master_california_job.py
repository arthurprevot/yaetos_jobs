from yaetos.etl_utils import ETL_Base, Commandliner
import pandas as pd
import numpy as np


class Job(ETL_Base):
    def transform(self, assets_dimension, emission_facts):
        query_str = """
            WITH
            assets_mod as (
                SELECT *
                FROM assets
                WHERE latitude > 32.5343 AND latitude < 42.0095
                  AND longitude > -124.4009 AND longitude < -114.1312
            ),
            emissions_mod as (
                SELECT Id, sum(co2) as co2
                FROM emissions
                WHERE year = 2022
                  AND co2 is not NULL
                GROUP BY Id
            ),
            joined as (
                SELECT at.*, co2
                FROM assets_mod at
                JOIN emissions_mod em on at.Id=em.Id
            )
            SELECT *
            FROM joined
            """
        dfs = {'assets': assets_dimension, 'emissions': emission_facts}
        df = self.query(query_str, engine='pandas', dfs=dfs)
        return df


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
