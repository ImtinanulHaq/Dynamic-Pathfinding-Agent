
import time

class Metrics:
	def __init__(self):
		self.nodes_visited = 0
		self.path_cost = 0
		self.start_time = 0
		self.end_time = 0

	def start_timer(self):
		self.start_time = time.time()

	def stop_timer(self):
		self.end_time = time.time()

	def get_execution_time(self):
		return (self.end_time - self.start_time) * 1000

	def reset(self):
		self.nodes_visited = 0
		self.path_cost = 0
		self.start_time = 0
		self.end_time = 0
