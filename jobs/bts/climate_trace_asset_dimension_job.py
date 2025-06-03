from yaetos.etl_utils import ETL_Base, Commandliner


class Job(ETL_Base):
    def transform(self, climate_trace):
        old_token = 'access_token=pk.eyJ1IjoiZWFydGhyaXNlIiwiYSI6ImNsN3NkMGkzdjBibWYzb2xhZndnNDc1d20ifQ.e4eN5Ee2g4G-zYcOgM-VQg'  # hardcoded in data probably by mistake.
        df = climate_trace.drop(['EmissionsSummary', 'Owners', 'Confidence', 'year'], axis=1)
        df['latitude'] = df['Centroid'].apply(lambda ce: ce['Geometry'][1])
        df['longitude'] = df['Centroid'].apply(lambda ce: ce['Geometry'][0])
        df['Thumbnail_post'] = df['Thumbnail'].apply(lambda ce: ce.replace(old_token, ''))
        df = df.drop(['Thumbnail', 'SectorRanks', 'Centroid', 'offset_batch'], axis=1)

        # drop duplicates
        variable_field = 'year'
        key_fields = [col for col in df.columns if col != variable_field]
        df = df[key_fields].drop_duplicates()
        return df


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata_bts_climate.yml'}
    Commandliner(Job, **args)
