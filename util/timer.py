import time

class Timer:
	start_time = time.monotonic()

	def getElapsedTime(self):
		return time.monotonic() - self.start_time

	def reset(self):
		last_time = self.getElapsedTime()
		self.start_time = time.monotonic()
		return last_time