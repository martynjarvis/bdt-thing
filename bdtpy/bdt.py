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
        # weights to apply to training samples, updated on each
        # iteration of the boosting algo
        sigWeights = np.ones(self.nSig, dtype=float)
        bkgWeights = np.ones(self.nBkg, dtype=float)
        reweight = 1.0/(np.sum(sigWeights)+np.sum(bkgWeights))
        sigWeights *= reweight
        bkgWeights *= reweight 

        self.treeWeights = np.zeros(self.ntrees, dtype=float)

        for i in xrange(self.ntrees):

            #Build new tree
            #sigWeights
            newTree = Tree()
            newTree.load(self.sigData,self.bkgData,weights=(sigWeights,bkgWeights))
            newTree.build()
            self.dTrees.append(newTree) 

            # evaluate tree
            err = 0.0

            sigWrong = np.zeros(self.nSig)
            bkgWrong = np.zeros(self.nBkg)

            #print sigWeights

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

        results = np.zeros(self.ntrees, dtype=float)

        for i,dt in enumerate(self.dTrees):
            #results[i] = math.log(self.treeWeights[i])*dt.classify(event)
            results[i] = self.treeWeights[i]*dt.classify(event)

        return np.sum(results)*(1.0/np.sum(self.treeWeights))
        
