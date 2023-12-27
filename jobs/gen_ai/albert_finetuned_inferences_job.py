from yaetos.etl_utils import ETL_Base, Commandliner, Path_Handler
# from transformers import file_utils
import tensorflow as tf
# import numpy as np
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

        # from transformers import TFAlbertForSequenceClassification
        # model = TFAlbertForSequenceClassification.from_pretrained(job_af.MODEL_NAME)


        evaluations = self.predict_all(model, text_to_classify)
        return evaluations

    def predict_all(self, model, text_to_classify):
        texts = text_to_classify['text'].tolist()
        texts_proc = job_af.preprocess(texts, job_af.MODEL_NAME)
        predictions = job_af.predict(model, texts_proc)
        # real = text_to_classify['classification'].tolist()
        # return pd.DataFrame({'texts': texts, 'predictions': predictions, 'real': real})
        return pd.DataFrame({'texts': texts, 'predictions': predictions})
    

if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
