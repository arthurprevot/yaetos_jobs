from yaetos.etl_utils import ETL_Base, Commandliner, Path_Handler
import tensorflow as tf
import pandas as pd
from albert_finetune_job import Job as job_af


class Job(ETL_Base):

    def transform(self, text_to_classify):
        # Force TensorFlow to use the CPU
        tf.config.set_visible_devices([], 'GPU')
        self.logger.info(f"Tensorflow devices: {tf.config.list_physical_devices()}")

        # Reload model
        path = self.jargs.input_model['path']
        path = Path_Handler(path, self.jargs.base_path, self.jargs.merged_args.get('root_path')).expand_later()
        model = job_af.reload_model(path)

        predictions = self.predict_all(model, text_to_classify)
        return predictions

    def predict_all(self, model, text_to_classify):
        texts = text_to_classify['text'].tolist()
        texts_proc = job_af.preprocess(texts)
        predictions = job_af.predict(model, texts_proc)
        return pd.DataFrame({'texts': texts, 'predictions': predictions})


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
