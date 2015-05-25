class IAPI(object):
	def name(self):
		raise NotImplementedError

	def auth(self, *args):
		raise NotImplementedError

	def getDevicesList(self):
		raise NotImplemented("error")

	def getDeviceInfo(self, data):
		raise NotImplemented("error")