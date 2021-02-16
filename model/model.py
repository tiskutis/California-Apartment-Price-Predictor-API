import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np


def preprocessing(data: pd.DataFrame) -> pd.DataFrame:
    """
    Input dataframe has some unnecessary columns, which are dropped.
    Price is divided by 1000 for better relationship with features.
    Trained model's r2 score is approximately 0.75
    :param data: pandas dataframe
    :return: modified pandas dataframe
    """
    data_copy = data
    data_copy.drop(['Unnamed: 0', 'Type', 'Lot size (acres)'], axis=1, inplace=True)
    data_copy.dropna(inplace=True)
    data_copy['Price'] = data_copy['Price'].div(1000)

    return data_copy


df = pd.read_csv('../data/California Housing.csv')
df_copy = preprocessing(df)

features = df_copy.drop(['Price'], 1)
label = np.round(df_copy['Price'])

std = StandardScaler()
lr = LinearRegression()

features = std.fit_transform(features)
X_train, X_test, y_train, y_test = train_test_split(features, label, test_size=0.1, random_state=42)
lr.fit(X_train, y_train)

with open("classifier.pkl", "wb") as cl_file:
    pickle.dump(lr, cl_file)

with open("scaler.pkl", "wb") as sc_file:
    pickle.dump(std, sc_file)