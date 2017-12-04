from taxi import *
from dispatch import *

from pg import DB

num_taxis = 10
# TODO: trips_per_min should be taken from all_results
trips_per_min = [1] * 1440

if __name__ == "__main__":
	db = DB(dbname='sust_comp_db', host='localhost', port = 5432, user='madikcan', passwd = 'qwert');
	d = Dispatch(db)

	taxis = []

	#  Trips are a tuple of ([long, lat], [long, lat], travel_time, distance, fare)
	for i in range(1440):
		print(i)
		d.timestep(i // 60, trips_per_min[i])
		while len(taxis) < num_taxis and len(d.trips) > 0:
			trip = d.trips.pop(0)
			taxis.append(Taxi(trip[0], 600, 700))

		for taxi in taxis:
			taxi.timestep()
			if taxi.is_idle() and len(d.trips) > 0:
				trip = d.dispatch_trip(taxi.coords)

	db.close()