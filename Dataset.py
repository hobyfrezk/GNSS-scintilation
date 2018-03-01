# Class: Dataset
# Usage: storage and operations of information about dataset
#
# Methods: 
#           void selectFeatures(features: List)                                                 Usage: generate X by setting List of features
#           void setTrainingAndTestDataset(.., .., percentage: Float, method: String)           Usage: generate training data and test data from total dataset by setting percentage of training data in total dataset and the method ('hard', 'random') to divide total dataset.
#           void setTrainingAndTestDataset(iTrain: List, iTest: List, .., ..)                   Usage: generate training data and test data from total dataset by selecting rows in total dataset.
#           void setTrainingAndTestSubDatasets(percentage: Float, method: String)               Usage: generate training data and test data from sub-dataset of all statellites by setting percentage of training data in total dataset and the method ('hard', 'random') to divide total dataset.
#           void setTrainingAndTestSubDataset(PRN: String, iTrain, iTest, percentage, method)   Usage: generate training data and test data from sub-dataset of statellite: PRN
#           CM: DataFrame getCorrelationMatrix()                                                Usage: get the correlation matrix of dataset


import pandas as pd
import numpy as np
import os
import time
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns


# The stucture Class used to storage information about dataset
class Dataset(object):

    # (not yet) Initalize the object with no parameters
    def __init__(self):
        pass

    # Load the dataset from the uri and automatically get the basic information about it
    def __init__(self,uri):
        (self.filepath, filenameWithType) = os.path.split(uri)          # String of filepath
        (self.filename,self.type) = os.path.splitext(filenameWithType)  # String of filename, String of file type
        self.dataset = pd.read_csv(uri)                 # Dataframe of stored dataset
        self.nRows = len(self.dataset.axes[0])          # Integer of rows count
        self.nColumns = len(self.dataset.axes[1])       # Integer of columns count
        self.features = self.dataset.axes[1]            # List of features
        if self.features[-1] == 'Scintillation':
            self.datasetType = 'supervised'             # String of dataset type (supervised or not)
            self.featuresWithoutScintillation = self.features[:-1]
        else:
            self.datasetType = 'unsupervised'
        # if the PRN of each row is known, create the sub-dataset of each satellite and nRows.
        self.hasPRN = False
        if 'SatNum' in self.features:
            self.hasPRN = True                              # Boolean of having feature PRN in features
            PRNCounter = Counter(self.dataset['SatNum'])    # Counter of the PRNs
            self.PRNList = dict(PRNCounter)                 # List of PRNs
            self.subDataset = {}                            # Dict of {PRN: matched dataset}
            self.nRowsSub = {}
            for PRN in self.PRNList:
                self.subDataset[PRN] = self.dataset[self.dataset['SatNum']==PRN]
                self.nRowsSub[PRN] = PRNCounter[PRN]
        
        # if date information is included in the dataset, record the dates in a list:
        self.hasDate = False
        if 'Date' in self.features:
            self.hasDate = True                             # Boolean of having feature Date in features
            DateCounter = Counter(self.dataset['Date'])     # Counter of the dates
            self.DateList = dict(DateCounter)               # List of dates

        # Initialize estimated Y and estimated subY
        self.YEst = None            # Numpy representation of estimated Y in dataset
        if self.hasPRN:
            self.subYEst = {}       # Dict of {PRN: matched YEst}
            for PRN in self.PRNList:
                self.subYEst[PRN] = None
        # Set X and subX
        self.selectFeatures(self.features[:-1])
        # Set training and test datasets: XTraining, YTraining, XTest, YTest
        if self.datasetType == 'supervised':
            self.setTrainingAndTestDataset(method = 'hard')

        # Set the training and test datasets for satellites
        self.isTrainingAndTestSubDatasets = False
        self.setTrainingAndTestSubDatasets()

    # (not yet) Load a dataset from a uri.
    def readDatasetFromFile(self,uri):
        pass

    # (not yet) write the dataset to a uri, all or just data with scintillation.
    def writeDatasetToFile(self,uri,type = 'scintillation'):      # type: 'all' or 'scintillation'
        pass

    # select features used in training and test, or predict (set X)
    def selectFeatures(self, features):
        self.selectedFeatures = features
        self.X = self.dataset[self.selectedFeatures].values
        if self.hasPRN:
            self.subX = {}                                  # Dict of {PRN: matched X}
            for PRN in self.PRNList:
                self.subX[PRN] = self.subDataset[PRN][self.selectedFeatures].values
            
    # define the training and test dataset by selecting percentage of rows used for training and methods with different method, or by given indexes of training data and test data
    def setTrainingAndTestDataset(self, iTrain = [], iTest = [], percentage = 0.8, method = 'select'):    # percentage: percentage of rows used for training.  method: 'hard', 'random' or 'select' 
        if self.datasetType == 'unsupervised':
            print 'You cannot set training and test subsets for an unsupervised dataset.'
            return -1
        self.Y = self.dataset['Scintillation'].values # Numpy representation of Y in dataset
        self.YEstTrain = None                           # Numpy representation of estimated Y predicted from XTrain
        self.YEstTest = None                            # Numpy representation of estimated Y predicted from XTest
        if method == 'hard':
            self.XTrain = self.X[:int(percentage*self.nRows)]       # Numpy representation of X used for training in dataset
            self.XTest = self.X[int(percentage*self.nRows):]        # Numpy representation of X used for test in dataset
            self.YTrain = self.Y[:int(percentage*self.nRows)]       # Numpy representation of Y used for training in dataset
            self.YTest = self.Y[int(percentage*self.nRows):]        # Numpy representation of Y used for test in dataset
            self.iTrain = range(0,int(percentage*self.nRows)-1)
            self.iTest = range(int(percentage*self.nRows),len(self.Y))
        elif method == 'random':
            iTrain = random.sample(range(self.nRows),int(percentage*self.nRows))
            iTest = []
            for i in range(self.nRows):
                if i not in iTrain:
                    iTest.append(i)
            self.XTrain = self.X[iTrain]
            self.XTest = self.X[iTest]
            self.YTrain = self.Y[iTrain]
            self.YTest = self.Y[iTest]
            self.iTrain = iTrain
            self.iTest = iTest
        elif method == 'select':
            if iTest == []:
                for i in range(self.nRows):
                    if i not in iTrain:
                        iTest.append(i)
            self.XTrain = self.X[iTrain]
            self.XTest = self.X[iTest]
            self.YTrain = self.Y[iTrain]
            self.YTest = self.Y[iTest]
            self.iTrain = iTrain
            self.iTest = iTest
          
    # set the training and test datasets for satellites
    def setTrainingAndTestSubDatasets(self, percentage = 0.8, method = 'hard'):
        if self.hasPRN:
            self.isTrainingAndTestSubDatasets = True
            self.subY = {}                              # Dict of {PRN: matched Y}
            self.subXTrain = {}                         # Dict of {PRN: matched XTrain}
            self.subXTest = {}                          # Dict of {PRN: matched XTest}
            self.subYTrain = {}                         # Dict of {PRN: matched YTrain}
            self.subYTest = {}                          # Dict of {PRN: matched YTest}
            self.subYEstTrain = {}                      # Dict of {PRN: matched YEstTrain}
            self.subYEstTest = {}                       # Dict of {PRN: matched YEstTest}
            self.iSubTrain = {}
            self.iSubTest = {}
            for PRN in self.PRNList:
                self.subY[PRN] = self.subDataset[PRN]['Scintillation'].values
                self.subYEstTrain[PRN] = None
                self.subYEstTest[PRN] = None
                self.setTrainingAndTestSubDataset(PRN = PRN, percentage = percentage, method = method)  # create the training and test dataset for each satellite by default auguments

    # define the training and test dataset for a single satellite by selecting percentage of rows used for training and methods with different method, or by given indexes of training data and test data
    def setTrainingAndTestSubDataset(self, PRN, iTrain = [], iTest = [], percentage = 0.8, method = 'select'):    # PRN: PRN of satellite, percentage: percentage of rows used for training.  method: 'hard', 'random' or 'select'
        if self.hasPRN:
            if PRN in self.PRNList:
                if method == 'hard':
                    self.subXTrain[PRN] = self.subX[PRN][:int(percentage*self.nRowsSub[PRN])]
                    self.subXTest[PRN] = self.subX[PRN][int(percentage*self.nRowsSub[PRN]):]
                    self.subYTrain[PRN] = self.subY[PRN][:int(percentage*self.nRowsSub[PRN])]
                    self.subYTest[PRN] = self.subY[PRN][int(percentage*self.nRowsSub[PRN]):]
                    self.iSubTrain[PRN] = range(0,int(percentage*self.nRowsSub[PRN])-1)
                    self.iSubTest[PRN] = range(int(percentage*self.nRowsSub[PRN]),len(self.subY[PRN]))
                elif method == 'random':
                    iTrain = random.sample(range(self.nRows),int(percentage*self.nRowsSub[PRN]))
                    iTest = []
                    for i in range(self.nRowsSub[PRN]):
                        if i not in iTrain:
                            iTest.append(i)
                    self.subXTrain[PRN] = self.subX[PRN][iTrain]
                    self.subXTest[PRN] = self.subX[PRN][iTest]
                    self.subYTrain[PRN] = self.subY[PRN][iTrain]
                    self.subYTest[PRN] = self.subY[PRN][iTest]
                    self.iSubTrain[PRN] = iTrain
                    self.iSubTest[PRN] = iTest
                elif method == 'select':
                    if iTest == []:
                        for i in range(self.nRowsSub[PRN]):
                            if i not in iTrain:
                                iTest.append(i)
                    self.subXTrain[PRN] = self.subX[PRN][iTrain]
                    self.subXTest[PRN] = self.subX[PRN][iTest]
                    self.subYTrain[PRN] = self.subY[PRN][iTrain]
                    self.subYTest[PRN] = self.subY[PRN][iTest]
                    self.iSubTrain[PRN] = iTrain
                    self.iSubTest[PRN] = iTest

    def getCorrelationMatrix(self):
        correlation_matrix = self.dataset.corr()
        ##plot the correlation matrix using heatmap
        sns.heatmap(correlation_matrix,xticklabels=correlation_matrix.columns.values,
            yticklabels=correlation_matrix.columns.values,square=True,Linewidth=0.5,annot=True,fmt=".2f",cmap='RdBu_r')
        plt.show()
        plt.yticks(rotation=0)
        return self.dataset.corr()




