from node import Node
from gini import weightedGini,vecWeightedGini

import numpy as np

class Tree():
    """
    represents the tree
    """

    def __init__(self, *items, **kw):
        """
        Create a Decision Tree
        """
        # Paramaters
        self.maxNodes = 1000
        self.nCuts = 20
        self.nEventsMin = -1
        self.maxDepth = 5
        self.rootNode = None

        # Counting stuff
        self.nNodes = 0

    def load(self,sigData,bkgData,weights=None):
        """
        load the data samples that are used
        """
        self.sigData = sigData
        self.bkgData = bkgData
        self.sigWeights = weights[0]
        self.bkgWeights = weights[1]
        #print weights[0]

        self.nVars = sigData.shape[1]
        self.nSig = sigData.shape[0]
        self.nBkg = bkgData.shape[0]

        if self.nEventsMin<=0 :
            self.nEventsMin = max(20,(self.nSig+self.nBkg)/(self.nVars*self.nVars*10))

    def build(self,node=None,sigMask=None,bkgMask=None):
        """
        Builds a decision tree from training data
        Recursivly creates a node and then finds the cut which gives the greatest separation
        between signal and background. Then applies the cut and creates two daughter nodes 
        that are then trained on a masked input sample.
        """

        # create root node for tree
        if node == None:
            node = Node()
            self.rootNode = node
            self.rootNode.root = True
            self.rootNode.depth = 0
            self.nNodes +=1

        # create a mask for the training samples, we will only train on events that 
        # pass the previous nodes
        if sigMask == None :
            sigMask = np.ones(self.nSig, dtype=bool)
        if bkgMask == None :
            bkgMask = np.ones(self.nBkg, dtype=bool)
        
        # check parameters, this may be a leaf...
        leafNode = False
        if self.nNodes >= self.maxNodes :
            leafNode = True

        if node.depth >= self.maxDepth : 
            leafNode = True

        sigEvents = long(np.sum(sigMask))
        bkgEvents = long(np.sum(bkgMask))

        if sigEvents + bkgEvents < 2*self.nEventsMin:
            leafNode = True

        if sigEvents<=0 or  bkgEvents<=0:
            leafNode = True

        # if this is a leaf node, set the return value for the node and then return
        if leafNode :
            node.leaf = True
            if float(sigEvents)/(sigEvents+bkgEvents) > 0.5:
                node.retVal = 1
            else :
                node.retVal = -1
            return 

        # Scan over each cut value of each variable to find cut which offers the best separation
        bestGini=-1.
        bestVar = -1
        bestCutVal = -1.
        
        parentIndex = weightedGini(sigEvents,bkgEvents)

        for var in xrange(self.nVars) :
            # use numpy histogram fn to find best cut value
            histRange = (
                min(self.bkgData[bkgMask,var].min(),self.sigData[sigMask,var].min()),
                max(self.bkgData[bkgMask,var].max(),self.sigData[sigMask,var].max())
                )
            bkgHist, bins = np.histogram(self.bkgData[bkgMask,var],self.nCuts,
                                           range=histRange,weights=self.bkgWeights[bkgMask])
            bkgYield = np.cumsum(bkgHist, dtype=float)

            sigHist, bins = np.histogram(self.sigData[sigMask,var],bins,weights=self.sigWeights[sigMask])
            sigYield = np.cumsum(sigHist, dtype=float)

            # calculate the increase in the separation index between the parent node the daughter nodes
            leftIndex = vecWeightedGini(sigYield,bkgYield)
            rightIndex = vecWeightedGini(sigEvents-sigYield,bkgEvents-bkgYield)
            diff = (parentIndex - leftIndex - rightIndex)/(sigEvents+bkgEvents)
            maxInd = diff[:-1].argmax() 
            if diff[maxInd] >= bestGini  : 
                bestGini = diff[maxInd]
                bestVar = var
                bestCutVal = bins[maxInd+1] 

        # apply cut values to node
        node.setCuts(bestVar,bestCutVal)

        # create two daughter nodes
        self.nNodes+=2

        leftnode = Node()
        leftnode.parent = node
        node.left = leftnode
        node.left.depth = node.depth+1

        rightnode = Node()
        rightnode.parent = node
        node.right = rightnode
        node.right.depth = node.depth+1

        # copy the masks and update them with the results of the node
        sigMaskLeft = np.copy(sigMask)
        sigMaskRight = np.copy(sigMask)
        for i in xrange(self.nSig):
            if sigMask[i] :
                sigMaskLeft[i] = self.sigData[i,bestVar] < bestCutVal
                sigMaskRight[i] = ~sigMaskLeft[i]

        bkgMaskLeft = np.copy(bkgMask)
        bkgMaskRight = np.copy(bkgMask)
        for i in xrange(self.nSig):
            if bkgMask[i] :
                bkgMaskLeft[i] = self.bkgData[i,bestVar] < bestCutVal
                bkgMaskRight[i] = ~bkgMaskLeft[i]
        
        # recursivly call function on daughter nodes, and repeat the training, but with a further masked input sample
        self.build(node=leftnode,sigMask=sigMaskLeft,bkgMask=bkgMaskLeft)
        self.build(node=rightnode,sigMask=sigMaskRight,bkgMask=bkgMaskRight)

        return 

    def classify(self, event):
        """
        return signal or background for an event
        """
        return self.rootNode.classify(event)

    
    def classifyEvents(self, events):
        """
        return signal or background for several events
        """
        results = np.array([
                self.rootNode.classify(event) for event in events])
        return results


    def draw(self):
        """
        print tree structure to terminal
        """
        print "Printing Tree:"
        self.rootNode.draw()
        return 

