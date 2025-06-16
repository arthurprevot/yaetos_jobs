from yaetos.etl_utils import ETL_Base, Commandliner


class Job(ETL_Base):
    def transform(self, emissions):
        df_duplicated = emissions
        n = 25
        for _ in range(n):
            df_duplicated = df_duplicated.union(emissions)
        return df_duplicated


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
