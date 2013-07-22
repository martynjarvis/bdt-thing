from tree import Tree
import numpy as np
import math

class BDT():
    """
    represents the BDT, a collection of trees
    """

    def __init__(self, *items, **kw):
        """
        Create a BDT with some trees
        """
        self.dTrees = []
        self.ntrees = 50 # TODO
        self.beta = 0.5

    def load(self,sigData,bkgData):
        """
        load the data samples that are used
        """
        self.sigData = sigData
        self.bkgData = bkgData

        self.nVars = sigData.shape[1]
        self.nSig = sigData.shape[0]
        self.nBkg = bkgData.shape[0]

    def build(self):
        """
        Build each tree in the 'forest' of trees. After each iteration, evaluate the tree 
        and reweight the input sample such that incorrect events are weighted up and correct
        events are weighted down
        """
        # weights to apply to training samples, updated on each
        # iteration of the boosting algo, normalised to 1
        sigWeights = np.ones(self.nSig, dtype=float)
        bkgWeights = np.ones(self.nBkg, dtype=float)
        reweight = 1.0/(np.sum(sigWeights)+np.sum(bkgWeights))
        sigWeights *= reweight
        bkgWeights *= reweight 

        # Weight of each tree, strong classifers have higher weight
        self.treeWeights = np.zeros(self.ntrees, dtype=float)

        for i in xrange(self.ntrees):

            # build new tree
            newTree = Tree()
            newTree.load(self.sigData,self.bkgData,weights=(sigWeights,bkgWeights))
            newTree.build()
            self.dTrees.append(newTree) 

            # evaluate trees
            # keep track of each event
            err = 0.0
            sigWrong = np.zeros(self.nSig)
            bkgWrong = np.zeros(self.nBkg)

            for j in range(self.nSig):
                if newTree.classify(np.array((self.sigData[j,])))<0:
                    sigWrong[i]=1
                    err+=sigWeights[j]

            for j in range(self.nBkg):
                if newTree.classify(np.array((self.bkgData[j,])))>0:
                    bkgWrong[i]=1
                    err+=bkgWeights[j]

            alpha = self.beta*math.log((1.0-err)/err)
            print err,alpha
            corFactor = math.exp(-alpha)
            wrongFactor = math.exp(alpha)

            if (err<1e-20 or err >= 0.5):
                print "SOEMTHING WRONG!!"

            self.treeWeights[i] = alpha

            # reweight training samples
            for j in range(self.nSig):
                if sigWrong[j]:
                    sigWeights[j]*=wrongFactor
                else :
                    sigWeights[j]*=corFactor

            for j in range(self.nBkg):
                if bkgWrong[j]:
                    bkgWeights[j]*=wrongFactor
                else :
                    bkgWeights[j]*=corFactor

            # normalise weights
            reweight = 1.0/(np.sum(sigWeights)+np.sum(bkgWeights))
            sigWeights *= reweight
            bkgWeights *= reweight

    def classify(self, event):
        """
        classify a given event. Iterates over each tree in the forest and then
        returns the weighted average of the results
        """

        results = np.zeros(self.ntrees, dtype=float)

        for i,dt in enumerate(self.dTrees):
            results[i] = self.treeWeights[i]*dt.classify(event)

        return np.sum(results)*(1.0/np.sum(self.treeWeights))
        
