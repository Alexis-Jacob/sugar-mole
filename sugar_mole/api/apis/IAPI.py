class IAPI(object):
	def name(self):
		raise NotImplementedError

	def auth(self, *args):
		raise NotImplementedError