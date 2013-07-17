    

class BDT():
	"""
	represents the BDT, a collection of trees
	"""

	def __init__(self, *items, **kw):
		"""
		Create a BDT with some trees
		"""
		self.trees = []
		ntrees = 100 # TODO

		if not items :
			for i in xrange(ntrees):
				self.trees.append(Tree)
