from IAPI import IAPI

class NetAtmo(IAPI):
	def __init__(self):
		self.name = "netatmo"

	def name(self):
		return self.name