import json
import os

import pandas as pd
from flask import jsonify
from google.cloud import storage
import pickle
import logging
from io import StringIO

class FraudPredictor:
    def __init__(self):
        self.model = None

    def predict_single_record(self, prediction_input):
        logging.debug(prediction_input)
        if self.model is None:
            try:
                model_repo = os.environ['MODEL_REPO']
                file_path = os.path.join(model_repo, "model_assignment1.pkl")
                print(file_path)
                with open(file_path, 'rb') as model_file:
                    self.model = pickle.load(model_file) 
            except KeyError:
                print("MODEL_REPO is undefined")
                with open('model_assignment1.pkl', 'rb') as model_file:
                    self.model = pickle.load(model_file) 

        df = pd.read_json(StringIO(json.dumps(prediction_input)), orient='records')
        y_pred = self.model.predict(df)
        logging.info(y_pred[0])
        status = (y_pred[0] > 0.5)
        logging.info(type(status[0]))
        # return the prediction outcome as a json message. 200 is HTTP status code 200, indicating successful completion
        return jsonify({'result': str(status[0])}), 200
