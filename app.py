import sys
sys.executable
import pickle
import datetime
import logging
import math
import os
import pickle
import sys
from datetime import datetime
from flask import Flask, request,jsonify
import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin, TransformerMixin
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from RideValue import RideValueTransformer

app = Flask(__name__)

with open('lgb_estimator.pkl',"rb") as fin:
    estimator = pickle.load(fin) 


@app.route('/ride_value_estimator', methods=['POST'])
def ride_value_estimator():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.get_json()
        data_frame = pd.DataFrame(request.get_json())
        data_frame['start_time'] = pd.to_datetime(data_frame['start_time'])
        df_transformer = RideValueTransformer()
        data_frame = df_transformer.transform(data_frame)
        estimated_ride_values = estimator.predict(data_frame).tolist()
        for i in range(len(json)):
            json[i]['estimated_ride_values'] = estimated_ride_values[i]
        return jsonify(json)
    else:
        return 'Content-Type not supported!'

if __name__ == "__main__":
    app.run(debug=True)
