import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt 

toll = pd.read_csv('time_between_two_tolls.csv')

toll['ist_timestamp'] = toll['ist_timestamp'].apply(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
toll['loading_out_time'] = toll['loading_out_time'].apply(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') )
toll['hours']  = toll['ist_timestamp'] - toll['loading_out_time']
toll['hours'] = toll.hours.apply(lambda x:x.total_seconds()/3600)

toll['distance_travelled'] = 0.0
toll['time_taken'] = toll['hours']
toll['time_btn_tolls'] = 0

new_time = pd.DataFrame(columns=toll.columns.tolist())

for truck in toll.vehicle_no.unique().tolist():
    for st_time in toll[toll.vehicle_no == truck].start_date.unique().tolist():
        df = toll[(toll.vehicle_no == truck) & (toll.start_date == st_time)].sort_values('odometer_km')
        df.distance_travelled = df.odometer_km.diff()
        df.time_btn_tolls = df.hours.diff()
        new_time = new_time.append(df)


new_time = new_time.loc[new_time['distance_travelled'] != 0]
new_time = new_time.fillna(0)

new_time.loc[new_time['time_btn_tolls'] == 0, 'time_btn_tolls']  = new_time.loc[new_time['time_btn_tolls'] == 0, 'time_taken']  

new_time['distance_travelled_cummulative'] = 0

for truck in new_time.vehicle_no.unique().tolist():
    for st_time in new_time[new_time.vehicle_no == truck].start_date.unique().tolist():
        new_time.loc[(new_time['vehicle_no'] == truck) & (new_time['start_date'] == st_time), 'distance_travelled_cummulative'] = new_time.loc[(new_time['vehicle_no'] == truck) & (new_time['start_date'] == st_time)]['distance_travelled'].cumsum()



new_time['delivery_status'] = 0
new_time['start_date'] = new_time['start_date'].apply(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') )
new_time['eta'] = toll['eta'].apply(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') )
new_time['unloading_in_time'] = new_time['unloading_in_time'].apply(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') )

new_time['delivery_status'] = (new_time['unloading_in_time'] - new_time['loading_out_time']) - (new_time['eta'] - new_time['start_date'])

new_time['delivery_status'] = new_time['delivery_status'].apply(lambda x: x.total_seconds()/3600)

new_time['delivery'] = ''

new_time.loc[new_time['delivery_status'] > 24, 'delivery'] = 'delay'
new_time.loc[(new_time['delivery_status'] <= 24) & (new_time['delivery_status'] >= 0), 'delivery'] = 'on-time'
new_time.loc[(new_time['delivery_status'] < 0), 'delivery'] = 'early'

new_time.delivery = new_time.delivery.replace({'delay':3,'on-time':2,'early':1})

today_date = datetime.datetime.now()
today_date.strftime("%Y-%m-%d %H:%M:%S")
today = today_date.strftime("%Y-%m-%d %H:%M:%S")
new_time['today'] = datetime.datetime.strptime(today, '%Y-%m-%d %H:%M:%S')

new_time['days_from_now'] = new_time['today'] - new_time['start_date'] 
new_time['days_from_now'] = new_time['days_from_now'].apply(lambda x: x.days)

new_time['avg_travel_time'] = new_time['start_date'] + (new_time['unloading_in_time'] - new_time['start_date'])/2

new_time['month_of_travel'] = new_time['avg_travel_time'].apply(lambda x: x.month)

new_time['time_of_travel'] = new_time.ist_timestamp.apply(lambda x: x.hour)

new_time['day_of_travel'] = new_time['avg_travel_time'].apply(lambda x: x.weekday())

toll_freq = dict(new_time['toll_both'].value_counts())
new_time['toll_freq'] = new_time['toll_both']
new_time['toll_freq'] = new_time['toll_freq'].apply(lambda x: toll_freq[x] )
m = int(0.3 * new_time['toll_freq'].median())
new_time = new_time[(new_time['toll_freq'] > m)]
new_time.drop(['toll_freq'], axis=1, inplace=True)

new_time['median_timestamp'] = 0
for toll_b in new_time.toll_both.unique().tolist():
    new_time.loc[new_time['toll_both'] == toll_b, 'median_timestamp'] = new_time.loc[new_time['toll_both'] == toll_b]['time_taken'].median()

new_time['median_timestamp'] = new_time['median_timestamp'].apply(lambda x:datetime.timedelta(hours=x))
new_time['median_timestamp'] = new_time['median_timestamp'] + new_time['loading_out_time']

new_time['delay'] = new_time['ist_timestamp'] - new_time['median_timestamp']
new_time['delay'] = new_time['delay'].apply(lambda x: x.total_seconds()/3600)
new_time['loading_out_time'] = new_time['loading_out_time'].apply(lambda x: x.hour)


final_df = new_time[['toll_both','vehicle_no','loading_out_time','ist_timestamp','distance_travelled','distance_travelled_cummulative','time_of_travel','day_of_travel','month_of_travel','days_from_now','delivery','time_taken','delay','time_btn_tolls']]

final_df.to_csv('Processed_df.csv', index=False)
