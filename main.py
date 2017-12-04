import numpy as np
import pandas as p
from pg import DB
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import random
import datetime as dt

# Functions
def load_data():
    dataTypes = {'vendor_id': str, 'passenger_count': np.int32, 'trip_distance': float, 'pickup_longitude': np.float64,
                 'pickup_latitude': np.float64, 'rate_code': np.int32, 'dropoff_longitude': np.float64,
                 'dropoff_latitude': np.float64, 'payment_type': str, 'fare_amount': float, 'surcharge': float,
                 'mta_tax': float, 'tip_amount': float, 'tolls_amount': str, 'total_amount': float};
    dataFrame = p.read_csv('./data/yellow_tripdata_2013-05.csv', na_filter=False, low_memory=False);
    return dataFrame;

def fill_database(input_data, database):
    #finish this
    headers = ['vendor_id','pickup_datetime','dropoff_datetime',
               'passenger_count','trip_distance','pickup_longitude',
               'pickup_latitude','rate_code','store_and_fwd_flag',
               'dropoff_longitude','dropoff_latitude','payment_type','fare_amount',
               'surcharge','mta_tax','tip_amount','tolls_amount','total_amount']
    (rowNum, colNum) = input_data.shape;
    result = 0;
    for i in range(0, rowNum):
        insert = True;
        item = input_data.loc[i, :]
        for j in range(0, colNum-1):
            if j==7 or j == 8: continue;
            if item[j] == '':
                insert = False;
                break;

        if insert:
            result = database.insert('spatial_data', vendor_id=item[0],pickup_datetime=item[1],
                            dropoff_datetime=item[2],passenger_count=item[3],
                            trip_distance=item[4],pickup_longitude=item[5],
                            pickup_latitude=item[6],
                            dropoff_longitude=item[9],dropoff_latitude=item[10],
                            payment_type=item[11],fare_amount=item[12],surcharge=item[13],
                            mta_tax=item[14],tip_amount=item[15],tolls_amount=item[16],
                            total_amount=item[17]);


    return result;
#create table with all col-s except for
def create_table(database):
    status = -1;
    status = database.query("create table spatial_data(vendor_id varchar, pickup_datetime timestamp, dropoff_datetime timestamp, "
                   "passenger_count integer, trip_distance float8, pickup_longitude double precision, "
                   "pickup_latitude double precision, dropoff_longitude double precision,"
                   "dropoff_latitude double precision, payment_type varchar, fare_amount float8, surcharge float8, "
                   "mta_tax float8, tip_amount float8, tolls_amount float8, total_amount float8)")
    return status;

def draw_pickup_locations(databaseQuery):
    result = databaseQuery.getresult()
    print(len(result))
    # map = Basemap(projection='merc', lat_0=40.730610, lon_0=-73.935242, resolution='i',
    #               llcrnrlon=-74.157112, llcrnrlat=40.617463,
    #               urcrnrlon=-73.678879, urcrnrlat=40.940936
    #               );
    # map.drawcoastlines()
    # map.drawcountries()
    # map.fillcontinents(color='coral')
    # map.drawmapboundary()

    result = random.sample(result, 10000)
    print(result[0][1])
    # for i in range (0, len(result)):
    #     item = result[i]
    #     x, y = map(item[5], item[6])
    #     map.plot(x,y, 'bo', markersize=0.1);
    #     if i % 1000 == 0: print(i, "/", len(result))
    # plt.show()
    return 0;

def draw_dropoff_locations(databaseQuery):
    result = databaseQuery.getresult()
    map = Basemap(projection='merc', lat_0=40.730610, lon_0=-73.935242, resolution='i',
                  llcrnrlon=-74.157112, llcrnrlat=40.617463,
                  urcrnrlon=-73.678879, urcrnrlat=40.940936
                  );
    map.drawcoastlines()
    map.drawcountries()
    map.fillcontinents(color='coral')
    map.drawmapboundary()


    for i in range (0, len(result)):
        item = result[i]
        x, y = map(item[9], item[10])
        map.plot(x,y, 'bo', markersize=0.1);
    plt.show()
    return 0;

#query spatial data of pickups of specific period
# from_day - initial day to choose
def query_pickup_by_time(from_day, database, to_day=None, from_time=None, to_time=None):
    if isinstance(from_day, int) == False: return 0;
    if to_day is None:
        if isinstance(from_day, int) == False:return 0;
        query_result = database.query('select * from spatial_data where extract(day from pickup_datetime) = '
                                      + str(from_day));
    else:
        if isinstance(from_time, int) == False or from_time <= 0 or from_time is None: from_time =0;
        if isinstance(to_time, int) == False or to_time > 23 or to_time is None: to_time = 23;
        query_result = database.query('select * from (select * from spatial_data where extract(day from pickup_datetime) >= '
                                      + str(from_day)+' and extract(day from pickup_datetime) < '+ str(to_day)
                                      +') AS selected_days where extract(hour from pickup_datetime) >= '+str(from_time)
                                      +' and extract(hour from pickup_datetime) <='+str(to_time));
    return query_result;

#query spatial data of pickups of specific period
def query_dropoff_by_time(from_day, database, to_day=None, from_time=None, to_time=None):
    if isinstance(from_day, int) == False: return 0;
    if to_day is None:
        if isinstance(from_day, int) == False: return 0;
        query_result = database.query('select * from spatial_data where extract(day from dropoff_datetime) = '
                                      + str(from_day));
    else:
        if isinstance(from_time, int) == False or from_time <= 0 or from_time is None: from_time =0;
        if isinstance(to_time, int) == False or to_time > 23 or to_time is None: to_time = 23;
        query_result = database.query('select * from (select * from spatial_data where extract(day from dropoff_datetime) >= '
                                      + str(from_day)+' and extract(day from dropoff_datetime) < '+ str(to_day)
                                      +') AS selected_days where extract(hour from dropoff_datetime) >= '+str(from_time)
                                      +' and extract(hour from dropoff_datetime) <= '+str(to_time));
    return query_result;



# Gets first limit spatial data from database
# if limit is not specified queries all data
#
def query_all_data(database, limit=None):
    if limit is None:
        query_result = database.query('select * from spatial_data')
    else:
        try:
            limit = int(limit)
            query_result = database.query('select * from spatial_data limit '+str(limit));
        except ValueError:
            query_result = database.query('select * from spatial_data');


    return query_result;

# Database connection
db = DB(dbname='sust_comp_db', host='localhost',
        port = 5432, user='madikcan', passwd = 'qwert');

# Function calling
#print(create_table(db));
#data = load_data();
#fill_database(data, db);


#Check results
# print(data)
#print(db.get_tables())
#print(db.get_attnames('trips'))
#print("\nSpatial Data:")
#print(db.get_attnames('spatial_data'))
#db.query("drop table trips")
#query = query_pickup_by_time(from_day=15, to_day=18, from_time= 0, to_time=23, database=db);
#query = query_pickup_by_day(15, db);

#query = query_all_data(db, 1);
#print(query)

#draw_pickup_locations(query)


#db.close()