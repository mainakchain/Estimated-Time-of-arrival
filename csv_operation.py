# sorting csv file in the order of vehicle_no
from __future__ import division
import pandas as pd
import csv
import time
from datetime import datetime
from statistics import mean, median
from collections import namedtuple
from contextlib import closing
import MySQLdb


MyStruct = namedtuple("vehicle", "vehicle_no loading_out_time delivery_status")

def sort(file = "Bhiwadi_Data.csv", params = ['origin', 'destination', 'vehicle_no', 'loading_out_time', 'odometer_km', 'ist_timestamp']):
		df = pd.read_csv(file)
		df = df.sort_values(by = params)
		# df = df.sort_values(by = 'vehicle_no')
		df.to_csv('Full_List_sorted.csv', index=False)
		return "Full_List_sorted.csv"


def get_toll_visit_count(rows):
	tolls = {}

	for row in rows :
	    if row[2] not in tolls:
	    	tolls[row[2]] = 1;
	    else:
	    	tolls[row[2]] = tolls[row[2]] + 1;

	return tolls

def get_data_from_file(filename, vehicle_nos = None, delivery_status = None):
	
	fields = []
	rows = []

	with open(filename, 'r') as csvfile:
	    # creating a csv reader object
	    csvreader = csv.reader(csvfile)
	     
	    # extracting field names through first row
	    fields = csvreader.next()
	 
	    # extracting each data row one by one
	    for row in csvreader:
	    	rows.append(row)
	 
	    # get total number of rows
	    # print("Total no. of rows: %d"%(len(rows)))

	return rows

def append_time_taken(filename):

	vehicle_no = None
	loading_out_time = None
	
	time_taken = []
	distance_travelled = []
	delivery_status = []
	late_by_hrs = []

	distance_reference = None
	

	with open(filename, 'r') as csvfile:
	    # creating a csv reader object
	    csvreader = csv.reader(csvfile)
	    
	    fields = csvreader.next()
	    
	    # extracting each data row one by one
	    for row in csvreader:
	        if (not vehicle_no) or (vehicle_no != row[3]) or (not loading_out_time) or (loading_out_time != row[4]):
	        	# print "\n\n-----new vehicle-----"
	        	# print row[3] + " " + row[4]
	        	vehicle_no = row[3]
	        	loading_out_time = row[4]
	        	
	        	distance_travelled.append(0)
	        	distance_reference = float(row[5])

	        else:
	        	distance_travelled.append(float(row[5]) - distance_reference)
	        	
	        
	        time_taken_temp = datetime.strptime(row[6], "%Y-%m-%d %H:%M:%S") - datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
	        # store time_taken value as int in hrs
	        time_taken.append(time_taken_temp.total_seconds()/3600)

	        late_by_hrs_temp = (datetime.strptime(row[11], "%Y-%m-%d %H:%M:%S") - datetime.strptime(row[8], "%Y-%m-%d %H:%M:%S")) - (datetime.strptime(row[10], "%Y-%m-%d %H:%M:%S") - datetime.strptime(row[9], "%Y-%m-%d %H:%M:%S"))
	        late_by_hrs_temp = late_by_hrs_temp.total_seconds() / 3600

	        late_by_hrs.append(late_by_hrs_temp)

	        if late_by_hrs_temp >= round(12.0000, 3):
				delivery_status.append("late")

	        elif late_by_hrs_temp <= round(-12.0000, 3):
				delivery_status.append("early")
				
	        else:
				delivery_status.append("on-time")



	df = pd.read_csv(filename)

	new_column = pd.DataFrame({'late_by_hrs': late_by_hrs, 'delivery_status':delivery_status, 'time_taken': time_taken, 'distance_travelled': distance_travelled})
	df = df.merge(new_column, left_index = True, right_index = True)
	
	df.to_csv(filename)

# delete rows where some cloumns are empty
def del_row(file1 = "Bhiwadi_Data.csv"):
	file2 = "edited.csv"
	with open(file1, 'rb') as inp, open(file2, 'wb') as out:
	    writer = csv.writer(out)
	    for row in csv.reader(inp):
	        if row[5] != "":
	            writer.writerow(row)

	return file2


def get_vehicle_nos(filename = "consigner_trips.csv", origin = "Jamshedpur", destination = "Bhiwadi"):
	vehicle_nos = []

	with open(filename, 'r') as csvfile:
	    # creating a csv reader object
	    csvreader = csv.reader(csvfile)
	     
	    # extracting field names through first row
	    fields = csvreader.next()
	 
	    # extracting each data row one by one
	    for row in csvreader:
	    	if (row[2] == origin) and (row[3] == destination):
	 	       # print row[2], row[3], row[12]
	 	       # print ""
	 	       temp = MyStruct(row[1], row[8], row[12])
	 	       vehicle_nos.append(temp)
	 
	    # get total number of rows
	    # print("Total no. of rows: %d"%(csvreader.line_num))

	return vehicle_nos

# input is data read from csv file
# [orgin][destination][toll_both] = [instances][min][max][avg][median]
def create_hash(rows):

	time_taken_dict = {}
	dis_travel_dict = {}


	origin = rows[0][1]
	destination = rows[0][2]
	toll_both = rows[0][3]

	time_taken_dict[origin] = {}
	time_taken_dict[origin][destination] = {}
	time_taken_dict[origin][destination][toll_both] = []

	dis_travel_dict[origin] = {}
	dis_travel_dict[origin][destination] = {}
	dis_travel_dict[origin][destination][toll_both] = []


	for row in rows:

		if (origin != row[1]):
			origin = row[1]
			time_taken_dict[origin] = {}
			dis_travel_dict[origin] = {}

			destination = row[2]
			time_taken_dict[origin][destination] = {}
			dis_travel_dict[origin][destination] = {}

			toll_both = row[3]
			time_taken_dict[origin][destination][toll_both] = []
			dis_travel_dict[origin][destination][toll_both] = []

		elif (destination != row[2]):
			destination = row[2]
			time_taken_dict[origin][destination] = {}
			dis_travel_dict[origin][destination] = {}

			toll_both = row[3]
			time_taken_dict[origin][destination][toll_both] = []
			dis_travel_dict[origin][destination][toll_both] = []

		elif (toll_both != row[3]):
			toll_both = row[3]
			time_taken_dict[origin][destination][toll_both] = []
			dis_travel_dict[origin][destination][toll_both] = []



		dis_travel_dict[origin][destination][toll_both].append(float(row[15]))
		time_taken_dict[origin][destination][toll_both].append(float(row[17]))

	return dis_travel_dict, time_taken_dict

# input is dict object that contains list to do stat on it
# and table name toll_time_stat or toll_dis_stat
def insert_stat(dict, table_name):

	db = MySQLdb.connect(user = "root", passwd = "root", db = "eta_stat")

	# delete previous data 
	with closing(db.cursor()) as cursor:

		query = "delete from " + table_name + ";"

		
		cursor.execute(query)
		
		db.commit()

		print(cursor._last_executed)


	# find stat values
	for origin in dict:
		for destination in dict[origin]:
			for toll_both in dict[origin][destination]:

				max_val = max(dict[origin][destination][toll_both])
				min_val = min(dict[origin][destination][toll_both])
				instances = len(dict[origin][destination][toll_both])
				avg_val = sum(dict[origin][destination][toll_both])/instances
				median_val = median(dict[origin][destination][toll_both])


				# insert values in db
				with closing(db.cursor()) as cursor:

					query = "insert into " + table_name + " (origin, destination, toll_both, instances, min, max, avg, median) values (%s, %s, %s, %s, %s, %s, %s, %s);"

					
					cursor.execute(query, (origin, destination, toll_both, instances, min_val, max_val, avg_val, median_val))
					
					db.commit()

					print(cursor._last_executed)
						# raise

	db.close()


# input is rows read from csv file 
# output is initialize a table in db
# add vehicle info in table
def insert_vehicle_stat(rows):
	db = MySQLdb.connect(user = "root", passwd = "root", db = "eta_stat")

	# delete previous data 
	with closing(db.cursor()) as cursor:

		query = "delete from vehicle_stat;"

		
		cursor.execute(query)
		
		db.commit()

		print(cursor._last_executed)

	
	for row in rows:
		with closing(db.cursor()) as cursor:

			query = "insert into vehicle_stat (origin, destination, vehicle_no, loading_out_time, delivery_status, toll_both, time_taken) values (%s, %s, %s, %s, %s, %s, %s);"

			
			cursor.execute(query, (row[1], row[2], row[4], row[5], row[14], row[3], row[17]))
			
			db.commit()

			print(cursor._last_executed)

	db.close()


# fields=[origin', 'destination', 'toll_both', 'vehicle_no', 'loading_out_time', 'odometer_km', 'ist_timestamp', 'distance_from_toll', 'loading_in_time', 'start_date', 'eta', 'unloading_in_time', 'slug', 'delivery_status', 'distance_travelled', 'late_by_hrs', 'time_taken']
# index with one
# zero index is some unnamed id created by append func

filename = "time_between_two_tolls(3).csv"

# delete rows s.t. odometer_km is null
filename = del_row(filename)

filename = sort(filename)

append_time_taken(filename)

# sort on the basis of toll plaza
sort(file = filename, params = ['origin', 'destination', 'toll_both'])


rows = get_data_from_file(filename)

insert_vehicle_stat(rows)

dis_travel_dict, time_taken_dict = create_hash(rows)

insert_stat(time_taken_dict, "toll_time_stat")
insert_stat(dis_travel_dict, "toll_dis_stat")


