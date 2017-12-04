from utils import *
import random

class Dispatch:
	"""docstring for Dispatch"""
	def __init__(self, db):
		self.db = db
		trips = []

	# Returns the closest trip and distance to that trip
	def dispatch_trip(self, coords):
		# TODO: finds the closest trip with coords using haversine
		return [trips.pop(0), 0]


	# generate trips. Trips are a tuple of ([ong, lat], [long, lat], travel_time, distance, fare)
	def timestep(self, time, num_trips):
		query_result = self.db.query('select * from spatial_data where extract(hour from pickup_datetime) = ' + str(time) + 
			' order by random() limit ' + str(num_trips)).getresult()

		for r in query_result:
			# TODO: fare inclues toll charges
			trips.append([r[5], r[6]], [r[7], r[8]], r[2].minute - r[1].minute + 1, r[4] * 1.60934, r[15])