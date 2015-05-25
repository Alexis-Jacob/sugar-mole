from IAPI import IAPI

class NetAtmo(IAPI):
	def __init__(self):
		self.name = "sen.se"

	def name(self):
		return self.name