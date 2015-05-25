from IAPI import IAPI

class NetAtmo(IAPI):
	def __init__(self):
		self.name = "my fox"

	def name(self):
		return self.name