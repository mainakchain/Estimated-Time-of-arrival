#import packages

import sqlite3
import numpy as np
import mysql.connector
import pandas as pd
import getpass
import seaborn as sns
import matplotlib.pyplot as plt
import plotly
import plotly.figure_factory as ff
from scipy import stats
# from sklearn.utils import shuffle
from sklearn.neural_network import MLPRegressor
# from sklearn.neural_network import MLPClassifier
# # from sklearn.ensemble import RandomForestRegressor
# from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import timedelta
from sklearn.ensemble import RandomForestRegressor
import datetime
import holidays
from sklearn.model_selection import cross_val_score
from sklearn.metrics import median_absolute_error
from sklearn.model_selection import GridSearchCV
# from sklearn.cross_validation import StratifiedKFold
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
# from sklearn.svm import LinearSVR
# from sklearn.svm import SVR
import pickle
import operator


#rev_dict_vehicle_no
#new_toll_dict_time_cum
#test_toll_list
new_toll_dict_time = {}
x_time = {}
new_toll_dict_time_cum = {}
x_time_cum = {}
new_toll_dict_dist = {}
x_dist = {}
new_toll_dict_dist_cum = {}
x_dist_cum = {}

test_toll_list = []

rev_dict_vehicle_no = {}

def change_vehicle_no_to_dummy(df):
    num = 1
    dict_vehicle_no = {}
    for truck in df['vehicle_no'].unique().tolist():
        df['vehicle_no'] = df['vehicle_no'].replace({truck: num})
        dict_vehicle_no[num] = truck
        num += 1
    return dict_vehicle_no


def find_toll_num(df):

    toll_dict_time = {}
    new_toll_dict_time = {}
    toll_dict_time_cum = {}
    new_toll_dict_time_cum = {}
    toll_dict_dist = {}
    new_toll_dict_dist = {}
    toll_dict_dist_cum = {}
    new_toll_dict_dist_cum = {}
    x_time = {}
    x_time_cum = {}
    x_dist = {}
    x_dist_cum = {}

    num = 1
    for toll in df.toll_both.unique().tolist():
        t = df['time_btn_tolls'][df.toll_both == toll].median()
        toll_dict_time[toll] = t
    
    for key, value in sorted(toll_dict_time.iteritems(), key=lambda (k,v): (v,k)):
        x_time[key] = value
        new_toll_dict_time[key] = num
        num+=1
        
    num = 1
    for toll in df.toll_both.unique().tolist():
        t = df['time_taken'][df.toll_both == toll].median()
        toll_dict_time_cum[toll] = t
    
    for key, value in sorted(toll_dict_time_cum.iteritems(), key=lambda (k,v): (v,k)):
        x_time_cum[key] = value
        new_toll_dict_time_cum[key] = num
        num+=1
        
    num = 1
    for toll in df.toll_both.unique().tolist():
        t = df['distance_travelled'][df.toll_both == toll].median()
        toll_dict_dist[toll] = t
    
    for key, value in sorted(toll_dict_dist.iteritems(), key=lambda (k,v): (v,k)):
        x_dist[key] = value
        new_toll_dict_dist[key] = num
        num+=1
        
    num = 1
    for toll in df.toll_both.unique().tolist():
        t = df['distance_travelled_cummulative'][df.toll_both == toll].median()
        toll_dict_dist_cum[toll] = t
    
    for key, value in sorted(toll_dict_dist_cum.iteritems(), key=lambda (k,v): (v,k)):
        x_dist_cum[key] = value
        new_toll_dict_dist_cum[key] = num
        num+=1

        
    return new_toll_dict_time, x_time, new_toll_dict_time_cum,x_time_cum,new_toll_dict_dist, x_dist, new_toll_dict_dist_cum, x_dist_cum


def train_dataset_extraction(df):

	new_toll_dict_time,x_time, new_toll_dict_time_cum, x_time_cum, new_toll_dict_dist, x_dist, new_toll_dict_dist_cum, x_dist_cum = find_toll_num(df)

	train_df = df[['toll_both','vehicle_no','loading_out_time','distance_travelled','time_of_travel','day_of_travel','month_of_travel','days_from_now','time_btn_tolls']]
	
	toll_list = sorted(x_dist_cum.items(), key=operator.itemgetter(1))
	test_toll_list = [i[0] for i in toll_list]

	train_df.toll_both = train_df.toll_both.replace(new_toll_dict_time_cum)

	dict_vehicle_no = change_vehicle_no_to_dummy(train_df)
	rev_dict_vehicle_no = dict((v,k) for k,v in dict_vehicle_no.iteritems())

	train_df = train_df.reset_index(drop=True)

	pickle_out = open("toll_list.pkl","wb")
	pickle.dump(new_toll_dict_dist_cum, pickle_out)
	pickle_out.close()

	pickle_out = open("vehicle_list.pkl","wb")
	pickle.dump(rev_dict_vehicle_no, pickle_out)
	pickle_out.close()

	pickle_out = open("test_toll_list.pkl","wb")
	pickle.dump(test_toll_list, pickle_out)
	pickle_out.close()

	pickle_out = open("x_dist.pkl","wb")
	pickle.dump(x_dist, pickle_out)
	pickle_out.close()

	pickle_out = open("x_time.pkl","wb")
	pickle.dump(x_time, pickle_out)
	pickle_out.close()


	return train_df


def algorithm_training(train_df):


	train_X = train_df.drop(['time_btn_tolls'], axis=1)
	train_y = train_df.time_btn_tolls

	X_train, X_test, y_train, y_test = train_test_split(train_X,train_y, test_size=0.3, random_state=42)

	scale= MinMaxScaler()
	X_train_scaled = scale.fit_transform(X_train)
	X_test_scaled = scale.fit_transform(X_test)

	reg_mlp = MLPRegressor(activation='logistic', alpha=4, batch_size='auto', beta_1=0.9,
       beta_2=0.999, early_stopping=False, epsilon=1e-08,
       hidden_layer_sizes=(100, 40), learning_rate='constant',
       learning_rate_init=0.001, max_iter=200, momentum=0.9,
       nesterovs_momentum=True, power_t=0.5, random_state=43, shuffle=True,
       solver='lbfgs', tol=0.0001, validation_fraction=0.1, verbose=False,
       warm_start=False)

	scores = cross_val_score(reg_mlp, X_train_scaled, y_train, scoring='neg_mean_squared_error', n_jobs=-1)
	print("Accuracy: %0.2f (+/- %0.2f)" % (np.abs(scores).mean(), scores.std() * 2))

	filename = 'finalized_model.sav'
	pickle.dump(reg_mlp, open(filename, 'wb'))

def main():

	df = pd.read_csv('Processed_df.csv') 							#importing the processed dataset
	train_df = train_dataset_extraction(df)

	algorithm_training(train_df)

if __name__ == '__main__':
	main()

	

