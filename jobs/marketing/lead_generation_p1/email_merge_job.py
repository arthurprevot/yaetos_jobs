from yaetos.etl_utils import ETL_Base, Commandliner


class Job(ETL_Base):
    def transform(self, companies, apollo):
        query_str = """
            WITH
            merged as (
                SELECT co.*, ap.*
                FROM companies co
                LEFT JOIN apollo ap on ap.company_url=co.url
            )
            SELECT *, count(*) OVER (partition by name) as nb_contact
            FROM merged
            order by name
            """
        dfs = {'companies': companies, 'apollo': apollo}
        df = self.query(query_str, engine='pandas', dfs=dfs)
        return df


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
