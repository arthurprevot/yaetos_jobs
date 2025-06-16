from yaetos.etl_utils import ETL_Base, Commandliner
from pyspark.sql.functions import array, explode, lit


class Job(ETL_Base):
    def transform(self, emissions):
        n = 7000
        df_duplicated = emissions.withColumn(
            "replicate", explode(array([lit(1)] * n))
        ).drop("replicate")        
        return df_duplicated


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
