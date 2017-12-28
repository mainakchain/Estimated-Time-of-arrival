#import packages
import sqlite3
import numpy as np
import mysql.connector
import pandas as pd
import getpass
import seaborn as sns
import matplotlib.pyplot as plt
import plotly
plotly.tools.set_credentials_file(username='mainakchain', api_key='B9m4DVrYYmsoW3jDSiok')
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
init_notebook_mode(connected=True)
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

df = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)

def import_dataset(df_name):
	df = pd.read_csv('SUPER_FINAL_DF.csv')

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


def data_preprocessing(df):
	df['distance_travelled_cummulative'] = 0

	for truck in df.vehicle_no.unique().tolist():
	    for st_time in df[df.vehicle_no == truck].loading_out_time.unique().tolist():
	        df.loc[(df['vehicle_no'] == truck) & (df['loading_out_time'] == st_time), 'distance_travelled_cummulative'] = df.loc[(df['vehicle_no'] == truck) & (df['loading_out_time'] == st_time)]['distance_travelled'].cumsum()

	new_toll_dict_time,x_time, new_toll_dict_time_cum, x_time_cum, new_toll_dict_dist, x_dist, new_toll_dict_dist_cum, x_dist_cum= find_toll_num(df)

	toll_list = sorted(x_dist_cum.items(), key=operator.itemgetter(1))
	test_toll_list = [i[0] for i in toll_list]



def train_test_df_building(df):

	today_date = datetime.datetime.now()
	vehicle = raw_input('Enter the vehicle no.: ')

	loading_out = raw_input('Enter the loading out time in %Y-%m-%d %H:%M:%S format: ')
	loading_out_delta = datetime.datetime.strptime(loading_out, '%Y-%m-%d %H:%M:%S')

	toll = raw_input('Latest Toll both: ')
	distance = input('Distance travelled from previous toll in km: ')
	ist = raw_input('IST Timestamp in %Y-%m-%d %H:%M:%S format: ')
	ist_delta = datetime.datetime.strptime(ist, '%Y-%m-%d %H:%M:%S')      
	ist_delta_given = ist_delta

	test_df= pd.DataFrame(columns=['toll_both','vehicle_no','loading_out_time', 'distance_travelled', 'time_of_travel',
	                                         'day_of_travel', 'month_of_travel', 'days_from_now'])
	prev_time = ist_delta

	if (toll == '') | (ist_delta == loading_out_delta):
	    a = []
	    for toll_ in test_toll_list :
	        b = []
	        distance = x_dist[toll_]
	        ist_delta = prev_time + timedelta(hours=x_time[toll_])
	        prev_time = ist_delta
	        b.extend([toll_, vehicle, loading_out_delta.hour, distance, ist_delta.hour, ist_delta.weekday(), ist_delta.month,
	                      (today_date - loading_out_delta).days])

	        a.append(b)

	    add_test_df = pd.DataFrame(a, columns= ['toll_both','vehicle_no','loading_out_time', 'distance_travelled', 'time_of_travel',
	                                         'day_of_travel', 'month_of_travel', 'days_from_now'])

	else:
	    i = test_toll_list.index(toll)
	    i = i+1
	    
	    a = []
	    while i != len(test_toll_list):
	        toll_ = test_toll_list[i]
	        b = []
	        distance = x_dist[toll_]
	        ist_delta = prev_time + timedelta(hours=x_time[toll_])
	        prev_time = ist_delta
	        b.extend([toll_, vehicle, loading_out_delta.hour, distance, ist_delta.hour, ist_delta.weekday(), ist_delta.month,
	                      (today_date - loading_out_delta).days])

	        a.append(b)
	        i = i + 1

	    add_test_df = pd.DataFrame(a, columns= ['toll_both','vehicle_no','loading_out_time', 'distance_travelled', 'time_of_travel',
	                                         'day_of_travel', 'month_of_travel', 'days_from_now'])

	test_df = test_df.append(add_test_df)
	train_df = df[['toll_both','vehicle_no','loading_out_time','distance_travelled','time_of_travel','day_of_travel','month_of_travel','days_from_now','time_btn_tolls']]

	new_toll_dict_time,x_time, new_toll_dict_time_cum, x_time_cum, new_toll_dict_dist, x_dist, new_toll_dict_dist_cum, x_dist_cum= find_toll_num(df)

	train_df.toll_both = train_df.toll_both.replace(new_toll_dict_time_cum)
	test_df.toll_both = test_df.toll_both.replace(new_toll_dict_time_cum)

	train_df = train_df.reset_index(drop=True)
	test_df = test_df.reset_index(drop=True)

	return train_df, test_df


def get_correlation_matrix(df):

	plt.figure(figsize=(9,9))
	# pivot_table = phase_1_2.pivot('helix1 phase', 'helix 2 phase','Energy')
	plt.xlabel('helix 2 phase', size = 15)
	plt.ylabel('helix1 phase', size = 15)
	plt.title('Energy from Helix Phase Angles', size = 15)
	sns.heatmap(df.corr(), annot=True, fmt=".1f", linewidths=.5, square = True, cmap = 'Blues_r')
	plt.show()


def algorithm_training(train_df, test_df):
	train_test_df = (train_df.drop(['time_btn_tolls'], axis=1)).append(test_df, ignore_index=True)
	dict_vehicle_no = change_vehicle_no_to_dummy(train_test_df)
	rev_dict_vehicle_no = dict((v,k) for k,v in dict_vehicle_no.iteritems())

	train_df['vehicle_no'] = train_df['vehicle_no'].replace(rev_dict_vehicle_no)
	test_df['vehicle_no'] = test_df['vehicle_no'].replace(rev_dict_vehicle_no)

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

	return reg_mlp


def model_pickling(model):
	#save the model using pickle model
	filename = 'finalized_model.sav'
	pickle.dump(reg_mlp, open(filename, 'wb'))

	with open('toll_list.pkl', 'wb') as f:
	    pickle.dump(new_toll_dict_dist_cum, f)

	with open('vehicle_list.pkl', 'wb') as f:
	    pickle.dump(rev_dict_vehicle_no, f)


def main():
	

