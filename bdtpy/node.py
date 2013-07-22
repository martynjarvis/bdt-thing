
class Node():
    """
    represents a branch in the tree
    """

    def __init__(self, *items, **kw):
        """
        Create a Node
        """
        # Tree parameters
        self.parent = None
        self.left = None
        self.right = None
        self.root = False
        self.leaf = False
        self.depth = 0 # 0 is root node

        # Node parameters (only set if node is not leaf)
        self.cutVar = -1
        self.cutVal = -1.0

        # Leaf parameters (only set if node is leaf)
        self.retVal = 0 # 1 if signal, -1 if bkg

    def classify(self,event):
        """
        Classify an event. If a leaf node, return retval otherwise apply 
        cuts and return daughter nodee
        """
        if self.leaf :
            return self.retVal

        if event[self.cutVar] < self.cutVal :
            return self.left.classify(event)
        else :
            return self.right.classify(event)

    def setCuts(self,var,val):
        """
        Save cut values on node
        """
        self.cutVar = var
        self.cutVal = val

    def draw(self,tabs=0):
        """
        print node, indention is given by depth in node
        """
    	if self.leaf==True :
    		if self.retVal == 1 :
    			print  tabs*"    ","Signal Leaf"
    		else :
    			print  tabs*"    ","Background Leaf"
    		return
    	print tabs*"    ", self.cutVar, self.cutVal
    	self.left.draw(tabs+1)
    	self.right.draw(tabs+1)