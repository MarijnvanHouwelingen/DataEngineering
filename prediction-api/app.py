import os

from flask import Flask, request

from fraud_predictor import FraudPredictor

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/fraud_predictor/model', methods=['PUT'])  # trigger updating the model
def refresh_model():
    return fp.download_model()

@app.route('/fraud_predictor/', methods=['POST'])  # path of the endpoint. Except only HTTP POST request
def predict_str():
    # the prediction input data in the message body as a JSON payload
    prediction_inout = request.get_json()
    return fp.predict_single_record(prediction_inout)

fp = FraudPredictor()
app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
