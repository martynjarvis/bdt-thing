
class Node():
    """
    represents a branch in the tree
    """

    def __init__(self, *items, **kw):
        """
        Create a Node
        """
        #print "Init node."
        self.parent = None
        self.left = None
        self.right = None
        self.root = False
        self.leaf = False

        # cuts the node applies
        self.cutVar = -1
        self.cutVal = -1.0

        # the values the node return if its a leaf
        self.retVal = -1 # 1 if signal, 0 if bkg

    def classify(self,event):

        if self.leaf :
            return self.retVal

        if event[self.cutVar] < self.cutVal :
            return self.left.classify(event)
        else :
            return self.right.classify(event)

    def setCuts(self,var,val):
        self.cutVar = var
        self.cutVal = val

    def draw(self,tabs=0):
    	if self.leaf==True :
    		if self.retVal == 1 :
    			print  tabs*"    ","Signal Leaf"
    		else :
    			print  tabs*"    ","Background Leaf"
    		return
    	print tabs*"    ", self.cutVar, self.cutVal
    	self.left.draw(tabs+1)
    	self.right.draw(tabs+1)