from flask import Flask, request
from model.preprocessing import process_input
import pickle
import json
from database import database

clf = pickle.load(open("model/classifier.pkl", "rb"))

app = Flask(__name__)


@app.route("/")
def greeting() -> str:
    """Initial message"""
    return 'Turing24 Project'


@app.route("/predict", methods=["POST"])
def predict() -> (str, int):
    """
    POST method runs this prediction function. Input is processed and scaled values are passed to pretrained linear
    regression algorithm. If prediction is successful, the original features together with predicted values are inserted
    into the database and response is given. If prediction failed, 400 error is returned together with exception message
    :param: None
    :return: Predicted values in json format. In case of error return error message and 400
    """
    request_data, input_params = process_input(request.data)

    try:
        predictions = clf.predict(input_params)
        predicted_prices = [price*1000 for price in predictions.tolist()]
    except Exception as err:
        return json.dumps({"Error": f"Prediction failed. Message: {err}"}), 500

    database.insert_in_table(json.dumps({"features": request_data}),
                             json.dumps({"Predicted values": predicted_prices}))

    return json.dumps({"Predicted values": predicted_prices})


@app.route("/select", methods=["GET"])
def get_last_10_records() -> str:
    """
    Selects last 10 records from the request-response database
    :return: last 10 requests and responses.
    """
    return json.dumps({"Last 10 records": database.select_from_table()})
