import numpy as np
import json
import pickle

scaler = pickle.load(open('model/scaler.pkl', "rb"))


def process_input(request_data: str) -> (list, np.array):
    """
    Inference pipeline. Scales input values which can then be passed to machine learning algorithm
    :param request_data: str, which contains json
    :return: features: list type with dictionary in it, which has the original input values
             scaled_values: np array which can be passed to machine learning algorithm
    """
    features = json.loads(request_data)["features"]
    scaled_values = scaler.transform(np.asarray([np.fromiter(features[i].values(),
                                                             dtype=float) for i in range(len(features))]))

    return features, scaled_values
