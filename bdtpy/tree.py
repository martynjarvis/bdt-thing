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
        self.maxNodes = 4
        self.nCuts = 20
        self.nEventsMin = 20
        self.rootNode = None

        # Counting stuff
        self.nNodes = 0


    def load(self,sigData,bkgData):
        """
        load the data samples that are used
        """
        self.sigData = sigData
        self.bkgData = bkgData

        self.nVars = sigData.shape[1]
        self.nSig = sigData.shape[0]
        self.nBkg = bkgData.shape[0]

        #self.nEventsMin = max(20,(self.nSig+self.nBkg)/(self.nVars*self.nVars*10))

    def build(self,node=None,sigMask=None,bkgMask=None):
        """
        build decision tree from data
        recursivly creates a node and splits in two
        """

        # create root node for tree
        if node == None:
            node = Node()
            self.rootNode = node
            self.rootNode.root = True
            self.nNodes +=1

        if sigMask == None :
            sigMask = np.ones(self.nSig, dtype=bool)
        if bkgMask == None :
            bkgMask = np.ones(self.nBkg, dtype=bool)
        
        print sigMask

        # check parameters, this may be a leaf...
        leafNode = False
        if self.nNodes >= self.maxNodes :
            leafNode = True

        #sigEvents = self.sigData[sigMask].shape[0]
        #bkgEvents = self.bkgData[sigMask].shape[0]

        sigEvents = np.bincount(sigMask,minlength=2)[1]
        bkgEvents = np.bincount(bkgMask,minlength=2)[1]

        #print sigEvents,bkgEvents

        if sigEvents + bkgEvents < self.nEventsMin:
            leafNode = True

        if leafNode :
            node.leaf = True
            if float(sigEvents)/(sigEvents+bkgEvents) > 0.5:
                node.retVal = 1.
            else :
                node.retVal = 0.
            return 

        bestGini=-1.
        bestVar = -1
        bestCutVal = -1.
        
        parentIndex = weightedGini(sigEvents,bkgEvents)
        #print parentIndex
        for var in xrange(self.nVars) :
            histRange = (
                min(self.bkgData[bkgMask,var].min(),self.sigData[sigMask,var].min()),
                max(self.bkgData[bkgMask,var].max(),self.sigData[sigMask,var].max())
                )

            bkgHist, bins = np.histogram(self.bkgData[bkgMask,var],self.nCuts,range=histRange)
            bkgYield = np.cumsum(bkgHist, dtype=float)

            sigHist, bins = np.histogram(self.sigData[sigMask,var],bins)
            sigYield = np.cumsum(sigHist, dtype=float)

            # print "~~~~"
            # print bins

            # print sigHist
            # print bkgHist

            # print sigYield
            # print bkgYield


            #rightIndex = gini(sigYield,bkgYield)
            #leftIndex

            leftIndex = vecWeightedGini(sigYield,bkgYield)
            rightIndex = vecWeightedGini(sigEvents-sigYield,bkgEvents-bkgYield)
            
            diff = (parentIndex - leftIndex - rightIndex)/(sigEvents+bkgEvents)
            # print diff
            maxInd = diff[:-1].argmax()
            if diff[maxInd] > bestGini :
                bestGini = diff[maxInd]
                bestVar = var
                bestCutVal = bins[maxInd+1] # +1? FIXME

        node.setCuts(bestVar,bestCutVal)
        #node.leaf = True # to fix

        #print bestCutVal

        self.nNodes +=2

        leftnode = Node()
        leftnode.parent = node
        node.left = leftnode

        rightnode = Node()
        rightnode.parent = node
        node.right = rightnode

        sigMaskLeft = np.array(sigMask,copy=True)
        sigMaskLeft = [(sigMask[i] and self.sigData[i,bestVar] < bestCutVal) for i in xrange(self.nSig)]
        bkgMaskLeft = np.array(bkgMask,copy=True)
        bkgMaskLeft = [(bkgMask[i] and self.bkgData[i,bestVar] < bestCutVal) for i in xrange(self.nBkg)]
        self.build(node=leftnode,sigMask=sigMaskLeft,bkgMask=bkgMaskLeft)

        sigMaskRight = np.array(sigMask,copy=True)
        sigMaskRight = [(sigMask[i] and self.sigData[i,bestVar] >= bestCutVal) for i in xrange(self.nSig)]
        bkgMaskRight = np.array(bkgMask,copy=True)
        bkgMaskRight = [(bkgMask[i] and self.bkgData[i,bestVar] >= bestCutVal) for i in xrange(self.nBkg)]
        self.build(node=rightnode,sigMask=sigMaskRight,bkgMask=bkgMaskRight)

        return 

    def classify(self, event):
        return self.rootNode.classify(event)

