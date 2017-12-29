import numpy as np
import mysql.connector
import pandas as pd
from sklearn.preprocessing import StandardScaler
from datetime import timedelta
import datetime
from sklearn.metrics import median_absolute_error
from sklearn.preprocessing import MinMaxScaler
import pickle
import operator

# load the model from disk
filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))


#load the conversion lists
pickle_in = open("test_toll_list.pkl","rb")
loaded_test_toll_list = pickle.load(pickle_in)
# print loaded_test_toll_list

pickle_in = open("toll_list.pkl","rb")
loaded_new_toll_dict_dist_cum = pickle.load(pickle_in)
# print loaded_new_toll_dict_dist_cum

pickle_in = open("vehicle_list.pkl","rb")
loaded_rev_dict_vehicle_no = pickle.load(pickle_in)
# print loaded_rev_dict_vehicle_no

pickle_in = open("x_dist.pkl","rb")
x_dist = pickle.load(pickle_in)


pickle_in = open("x_time.pkl","rb")
x_time = pickle.load(pickle_in)


#make the test dataset

today_date = datetime.datetime.now()
vehicle = raw_input('Enter the vehicle no.: ')

loading_out = raw_input('Enter the loading out time in %Y-%m-%d %H:%M:%S format: ')
loading_out_delta = datetime.datetime.strptime(loading_out, '%Y-%m-%d %H:%M:%S')

toll = raw_input('Latest Toll both: ')
distance = input('Distance travelled from 1st toll in km: ')
ist = raw_input('IST Timestamp in %Y-%m-%d %H:%M:%S format: ')
ist_delta = datetime.datetime.strptime(ist, '%Y-%m-%d %H:%M:%S')      
ist_delta_given = ist_delta


new_test_df= pd.DataFrame(columns=['toll_both','vehicle_no','loading_out_time', 'distance_travelled', 'time_of_travel',
                                         'day_of_travel', 'month_of_travel', 'days_from_now'])
prev_time = ist_delta

if (toll == '') | (ist_delta == loading_out_delta):
    a = []
    for toll_ in loaded_test_toll_list :
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
    i = loaded_test_toll_list.index(toll)
    i = i+1
    
    a = []
    while i != len(loaded_test_toll_list):
        toll_ = loaded_test_toll_list[i]
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

new_test_df = new_test_df.append(add_test_df)
test_df = new_test_df.copy()


new_test_df['toll_both'] = new_test_df['toll_both'].replace(loaded_new_toll_dict_dist_cum)

if (vehicle in loaded_rev_dict_vehicle_no) == False:
	loaded_rev_dict_vehicle_no[vehicle] = (max(loaded_rev_dict_vehicle_no.iteritems(), key=operator.itemgetter(1))[1]) + 1
	pickle_out = open("vehicle_list.pkl","wb")
	pickle.dump(loaded_rev_dict_vehicle_no, pickle_out)
	pickle_out.close()

    
new_test_df['vehicle_no'] = new_test_df['vehicle_no'].replace(loaded_rev_dict_vehicle_no)

scale = MinMaxScaler()
X_predict_scaled = scale.fit_transform(new_test_df)
predictions = loaded_model.predict(X_predict_scaled)

show_df = test_df.copy()
show_df['predicted'] = predictions
show_df['eta'] = show_df['predicted'].cumsum()
show_df['eta'] = show_df['eta'].apply(lambda x: ist_delta_given + timedelta(hours=x) )

show_df.to_csv('predicted_eta.csv', index=False)

