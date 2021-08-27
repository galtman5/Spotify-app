import numpy as np
import pandas as pd
import sklearn
import feature_engine
from feature_engine.encoding import OneHotEncoder as fe_OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
import re
import joblib


def explicit_binarizer(x):
    if x == True:
        return 1
    else:
        return 0


def decade_function(x):
    if x in range(1900, 1991):
        return '1900-1990'
    elif x in range(1991, 1996):
        return '1991-1995'
    elif x in range(1996, 2001):
        return '1996-2000'
    elif x in range(2001, 2006):
        return '2001-2005'
    elif x == 2006:
        return '2006'
    elif x == 2007:
        return '2007'
    elif x == 2008:
        return '2008'
    elif x == 2009:
        return '2009'
    elif x == 2010:
        return '2010'
    elif x == 2011:
        return '2011'
    elif x == 2012:
        return '2012'
    elif x == 2013:
        return '2013'
    elif x == 2014:
        return '2014'
    elif x == 2015:
        return '2015'
    elif x == 2016:
        return '2016'
    elif x == 2017:
        return '2017'
    elif x == 2018:
        return '2018'
    elif x == 2019:
        return '2019'
    elif x == 2020:
        return '2020'
    elif x == 2021:
        return '2021'


def wrangle(df):
    df.drop(columns='Unnamed: 0', inplace=True)
    df['explicit'] = df['explicit'].apply(explicit_binarizer)
    df['age'] = df['year'].apply(decade_function)
    loaded_ohe = joblib.load('/content/ohe.joblib')
    df = loaded_ohe.transform(df.fillna('Missing'))
    # feature scailing for float columns in df3
    loaded_scaler = joblib.load('/content/scaler.joblib')
    scale_cols = ['danceability', 'energy', 'loudness', 'speechiness',
                  'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                  'time_signature', 'key', 'mode']
    scaled = df[scale_cols].reset_index(drop=True)
    scaler = loaded_scaler
    scaled_float_df = pd.DataFrame(
        scaler.transform(scaled), columns=scaled.columns)
    df.drop(columns=scale_cols, inplace=True)
    df = pd.concat([df, scaled_float_df], axis=1)
    df.drop(columns='year', inplace=True)
    return df
