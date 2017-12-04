# TODO: implement battery model and charge decision making

class Taxi:
	"""docstring for Taxi"""
	def __init__(self, coords, cur_range, max_range):
		self.coords = coords
		self.cur_range = cur_range
		self.max_range = max_range
		self.dest_coords = None
		self.travel_time = 0
		self.fare_total = 0
		self.trip = None
		self.velocity = 0
		self.waypoints = []

	def can_go_distance(self, distance):
		return self.cur_range > distance

	def is_idle(self):
		return self.trip == None

	def add_waypoint(self, trip):
		self.waypoints.append(trip)

	# Trips are a tuple of ([long, lat], [long, lat], travel_time, distance, fare)
	def set_destination(self, trip):
		self.trip = trip
		self.travel_time = travel_time
		self.velocity = [(trip[0][0] - self.coords[0])/travel_time, (trip[0][1] - self.coords[1])/travel_time]
		self.km_per_min = distance / travel_time

	def timestep(self):
		if self.travel_time	> 0:
			self.lat += self.velocity[0]
			self.long += self.velocity[1]
			self.travel_time -= 1
		
		if self.travel_time == 0 and self.trip:
			self.fare_total += trip[4]
			self.trip = None

	def __str__(self):
		return 'Location: {}, Range: {}/{}'.format(self.coords, self.cur_range, self.max_range)