import os
import csv
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.compose import ColumnTransformer
from apps.analysis import utils
from .utils import get_collection
from .utils import CROSS_DATA_COLLECTION, LONG_DATA_COLLECTION, MERGED_DATA, RF_RESULT, Y_RESULT


def load_data(command, dir, file_name, collection):
    working_dir = os.path.join(os.getcwd(), dir)
    file_path = os.path.join(working_dir, file_name)    
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            records = list(reader)
            if records:
                # Delete last data
                collection.delete_many({})
                # Insert new data
                collection.insert_many(records)
                command.write_suc(f'Successfully imported {file_name} documents into database.')
            else:
                command.write_warn('CSV file was empty or contained only headers.')

    except FileNotFoundError:
        command.write_err(f'Error: File not found at {file_path}')
        raise
        
    except Exception as e:
        command.write_err(f'An unexpected error occurred: {e}')
        raise

    return None


def train_and_store(command, dir):
    utils.USE_ASYNC_DB = False

    cross_collection = get_collection(CROSS_DATA_COLLECTION)
    long_collection = get_collection(LONG_DATA_COLLECTION)

    load_data(command, dir, file_name='cross.csv', collection=cross_collection)
    load_data(command, dir, file_name='long.csv', collection=long_collection)

    cursor = cross_collection.find({}, {'_id': 0})
    data_cross = pd.DataFrame(list(cursor))
    cursor = long_collection.find({}, {'_id': 0})
    data_long = pd.DataFrame(list(cursor))
    data = pd.concat([data_cross, data_long])

    data.replace(['', 'nan', 'null'], np.nan, inplace=True)
    for column in data.columns:
        mode_value = data[column].mode()[0]  
        data[column].fillna(mode_value, inplace=True)
    
    missing_values_after_filling = data.isnull().sum()
    
    X = data.drop(['Group', 'ID', 'Delay', 'Subject ID', 'MRI ID', 'Visit', 'MR Delay'], axis=1)
    y = data['Group']

    scale = ['Age', 'EDUC', 'SES', 'MMSE', 'CDR', 'eTIV','nWBV', 'ASF']
    ohe = ['M/F', 'Hand']
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = ColumnTransformer(
    transformers=[
        ('scale', StandardScaler(), scale),
        ('ohe', OneHotEncoder(), ohe)
    ])
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier())
    ])
    label = LabelEncoder()
    y_train_label = label.fit_transform(y_train)
    y_test_label = label.transform(y_val)
    pipeline.fit(X_train, y_train_label)
    accuracy = pipeline.score(X_val, y_test_label)

    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier())
    ])
    
    pipeline.fit(X_train, y_train_label)
    accuracy = pipeline.score(X_val, y_test_label)
    rf_rsult = classification_report(y_test_label, pipeline.predict(X_val))
    y_prob = pipeline.predict_proba(X_val)

    get_collection(RF_RESULT).replace_one({'_id':'latest'}, {'report':rf_rsult}, upsert=True)
    formatted_probs = y_prob.tolist() if hasattr(y_prob, 'tolist') else list(y_prob)
    get_collection(Y_RESULT).replace_one({'_id':'latest'}, {'y_prob':formatted_probs}, upsert=True)
    get_collection(MERGED_DATA).delete_many({})
    get_collection(MERGED_DATA).insert_many(data.to_dict('records'))

