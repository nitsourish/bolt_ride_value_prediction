import os.path
import pickle

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin, TransformerMixin
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

class RideValueTransformer(BaseEstimator, RegressorMixin, TransformerMixin):

    def transform(self, X):
        """This transforms the dataframe to the desired
         features and shape"""
        X['pickup_time'] = self.__add_time_feature(X)
        X['weekday'] = self.__add_weekdays_feature(X)
        X = self.__add_travel_features(X)
        X['distance'] = np.round(self.__add_distance_feature(X), 2)
        X = self.__drop_unrequired_fields(X)
        X = self.__normalize(X)
        return X

    def __add_travel_features(self, X):
        X['abs_diff_longitude'] = (X.end_lng - X.start_lng).abs()
        X['abs_diff_latitude'] = (X.end_lat - X.start_lat).abs()
        return X

    def __add_time_feature(self, X):
        return X['start_time'].dt.hour

    def __add_weekdays_feature(self, X):
        return X['start_time'].dt.day_of_week

    def __add_distance_feature(self, X):
        """Method for calculating distance from start lat/long to end lat/long"""
        radius_of_earth = 6373.0
        lat1 = np.asarray(np.radians(X['start_lat']))
        lon1 = np.asarray(np.radians(X['start_lng']))
        lat2 = np.asarray(np.radians(X['end_lat']))
        lon2 = np.asarray(np.radians(X['end_lng']))

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        distance = radius_of_earth * c

        distance_array = np.asarray(distance) * 0.621
        return pd.Series(distance_array)

    def __drop_unrequired_fields(self, X):
        return X.drop(['start_time', 'start_lat', 'start_lng', 'end_lat', 'end_lng'], axis=1)

    def __normalize(self, X):
        X['abs_diff_longitude'] = np.abs(
            X['abs_diff_longitude'] - np.mean(X['abs_diff_longitude']))
        X['abs_diff_longitude'] = X['abs_diff_longitude'] / np.var(X['abs_diff_longitude'])

        X['abs_diff_latitude'] = np.abs(
            X['abs_diff_latitude'] - np.mean(X['abs_diff_latitude']))
        X['abs_diff_latitude'] = X['abs_diff_latitude'] / np.var(X['abs_diff_latitude'])
        return X