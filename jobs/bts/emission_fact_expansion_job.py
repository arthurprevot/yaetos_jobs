"""Same as ex1_sql_job.sql but allows access to spark for more complex ops (not used here but in ex2_frameworked_job.py)."""
from yaetos.etl_utils import ETL_Base, Commandliner


class Job(ETL_Base):
    def transform(self, pageviews):
        df = pageviews
        df_duplicated = pageviews
        
        # # Perform the union operation n-1 times to achieve n duplications
        # n = 2
        # for _ in range(n - 1):
        #     df_duplicated = df_duplicated.union(df)

        # Perform the union operation n-1 times to achieve n duplications
        n = 5
        for _ in range(n - 1):
            df_duplicated = df_duplicated.union(df_duplicated)

        return df_duplicated


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
