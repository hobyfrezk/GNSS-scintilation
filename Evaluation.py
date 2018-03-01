import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from Dataset import Dataset
from Algorithm import Algorithm

class Evaluation(object):
    def __init__(self, dataset, algorithm):
        self.dataset = dataset
        self.algorithm = algorithm
        if self.dataset.hasPRN:
            self.scores_K_fold_PRN = {}
            self.mean_scores_K_fold_PRN = {}
            self.crossValSubDatasetTest = {}

    # evaluate K-fold cross validation score (accuracy_score, precision_score, recall_score, f1_score) for total dataset
    def getCrossValScores(self, K = 10):
        kf = KFold(K)
        scores_K_fold = pd.DataFrame()
        self.crossValDatasetTest = []
        for train, test in kf.split(self.dataset.X):
            self.dataset.setTrainingAndTestDataset(train, test)
            if max(self.dataset.YTrain) == 0:
                l = len(self.dataset.YTest)
                self.dataset.YEstTest = np.zeros((l,1))
            else:
                self.algorithm.fit(self.dataset.XTrain, self.dataset.YTrain)
                self.dataset.YEstTest = self.algorithm.predict(self.dataset.XTest)
            scores_K_fold = scores_K_fold.append(self.getScores(self.dataset.YTest, self.dataset.YEstTest), ignore_index=True)
            dataset = {}
            dataset['dataset'] = self.dataset.dataset.iloc[test]
            dataset['dataset'] = dataset['dataset'].assign(YEst = self.dataset.YEstTest)
            self.crossValDatasetTest.append(dataset)
        self.scores_K_fold = scores_K_fold
        self.mean_scores_K_fold = self.scores_K_fold.mean(axis = 0)
        self.scores_K_fold = self.scores_K_fold.round(3)
        self.mean_scores_K_fold = self.mean_scores_K_fold.round(3)
        self.crossValDatasetTestMergedPRN = self.splitDatasetByPRN(self.mergeDatasetList(self.crossValDatasetTest))
        return self.scores_K_fold
    
    # evaluate K-fold cross validation score (accuracy, sensitivity, specificity) for sub-dataset of all satellites if PRN is provided    
    def getCrossValScoresAllPRN(self, K = 10):
        if self.dataset.hasPRN:
            for PRN in self.dataset.PRNList:
                self.getCrossValScoresPRN(PRN, K)
            return self.scores_K_fold_PRN

    # evaluate K-fold cross validation score (accuracy, sensitivity, specificity) for sub-dataset of certain satellite if PRN is provided
    def getCrossValScoresPRN(self, PRN, K = 10):
        if not self.dataset.hasPRN:
            print 'No PRN information'
            return -1
        if not (PRN in self.dataset.PRNList):
            print 'No this PRN'
            return -1
        kf = KFold(min(K,len(self.dataset.subX[PRN])))
        scores_K_fold = pd.DataFrame()
        self.crossValSubDatasetTest[PRN] = []
        for train, test in kf.split(self.dataset.subX[PRN]):
            self.dataset.setTrainingAndTestSubDataset(PRN, train, test)
            if max(self.dataset.subYTrain[PRN]) == 0:
                l = len(self.dataset.subYTest[PRN])
                self.dataset.subYEstTest[PRN] = np.zeros((l,1))
            else:
                self.algorithm.fit(self.dataset.subXTrain[PRN], self.dataset.subYTrain[PRN])
                self.dataset.subYEstTest[PRN] = self.algorithm.predict(self.dataset.subXTest[PRN])
            scores_K_fold = scores_K_fold.append(self.getScores(self.dataset.subYTest[PRN], self.dataset.subYEstTest[PRN]), ignore_index=True)
            dataset = {}
            dataset['dataset'] = self.dataset.subDataset[PRN].iloc[test]
            dataset['dataset'] = dataset['dataset'].assign(YEst = self.dataset.subYEstTest[PRN])
            self.crossValSubDatasetTest[PRN].append(dataset)
        self.scores_K_fold_PRN[PRN] = scores_K_fold
        self.mean_scores_K_fold_PRN[PRN] = self.scores_K_fold_PRN[PRN].mean(axis = 0)
        return self.scores_K_fold_PRN[PRN]

    # evaluate scores for certain Y and estimated Y
    def getScores(self, Y, YEst):
        scores = {}
        scores['accuracy'] = accuracy_score(Y, YEst)
        if max(Y) < 0.5:
            scores['precision'] = np.nan
            scores['recall'] = np.nan
            scores['fi_score'] = np.nan
        elif max(YEst) < 0.5:
            scores['precision'] = np.nan
            scores['fi_score'] = np.nan
        else:
            scores['precision'] = precision_score(Y, YEst)
            scores['recall'] = recall_score(Y, YEst)
            scores['fi_score'] = f1_score(Y, YEst)
        return scores

    # show 10-fold valiation scores for total dataset and if exist, the scores for sub-dataset of each satellite
    def showAllCVS(self):
        # print 'Mean values of 10-fold valiation scores for total dataset:'
        self.getCrossValScores(K = 10)
        print self.scores_K_fold
        if self.dataset.hasPRN:
            self.getCrossValScoresAllPRN(K = 10)
            # print 'Mean values of 10-fold valiation scores for sub-dataset of each satellite:'
            for PRN in self.dataset.PRNList:
                print 'PRN '+str(PRN)+' :'
                print self.scores_K_fold_PRN[PRN]

    def plotAllKFoldPRN(self,PRN,features = ['S4','C/N0','Elevation'],date = 20150326):
        datasetAll = self.crossValSubDatasetTest[PRN]
        title = 'PRN_'+str(PRN)+'_DATE_'+ str(date)
        self.plotAllKFold(datasetAll, features, title, date)

    def plotAllKFold(self, datasetAll, features, title, date = 20150326):
        nFeatures = len(features)
        fig = plt.figure(figsize=(15, 1.8*nFeatures),facecolor = 'grey')
        fig.suptitle(title)
        sp = []
        for i in range(nFeatures):
            sp.append(fig.add_subplot(nFeatures,1,i+1))
            for dataset in datasetAll:
                time = dataset['dataset'].loc[dataset['dataset']['Date'] == date]['GPS time']
                Y = dataset['dataset'].loc[dataset['dataset']['Date'] == date]['Scintillation']
                YEst = dataset['dataset'].loc[dataset['dataset']['Date'] == date]['YEst']
                dataFeature = dataset['dataset'].loc[dataset['dataset']['Date'] == date][features[i]]
                sp[i].plot(time[Y > 0.5],dataFeature[Y > 0.5],'r.')
                sp[i].plot(time[Y <= 0.5],dataFeature[Y <= 0.5],'b.')
                sp[i].plot(time[YEst > 0.5], YEst[YEst > 0.5]*0,'m.')
                sp[i].plot(time[YEst <= 0.5], YEst[YEst <= 0.5]*0,'y.')
            sp[i].grid(True)
            sp[i].set_xlabel('GPS Time')
            sp[i].set_ylabel(features[i])
            sp[i].legend(['Scin.','No Scin.','Est Scin.','Est no Scin.'],bbox_to_anchor=(1, 0.5),loc='center left')
        plt.savefig('figures/'+title+'.jpg')
        plt.show()

    def mergeDatasetList(self, dataset_list):
        mergedDataset = pd.DataFrame()
        for dataset in dataset_list:
            mergedDataset = mergedDataset.append(dataset['dataset'], ignore_index = True)
        return mergedDataset

    def splitDatasetByPRN(self,dataset):
        if self.dataset.hasPRN:
            crossValDatasetTestMergedPRN = {}
            for PRN in self.dataset.PRNList:
                crossValDatasetTestMergedPRN[PRN] = dataset[dataset['SatNum']==PRN]
        return crossValDatasetTestMergedPRN

    
    def getCVDTMPRN(self,PRN):
        return self.crossValDatasetTestMergedPRN[PRN]

    # Use this to get plot of certain PRN
    def plot_PRN_Date(self, PRN, features = ['S4','C/N0','Elevation'], date = 20150326):
        dataset = self.getCVDTMPRN(PRN)
        title = 'PRN_'+str(PRN)+'_DATE_'+ str(date)
        nFeatures = len(features)
        fig = plt.figure(figsize=(15, 1.8*nFeatures),facecolor = 'grey')
        fig.suptitle(title)
        sp = []
        for i in range(nFeatures):
            sp.append(fig.add_subplot(nFeatures,1,i+1))
            time = dataset.loc[dataset['Date'] == date]['GPS time']
            Y = dataset.loc[dataset['Date'] == date]['Scintillation']
            YEst = dataset.loc[dataset['Date'] == date]['YEst']
            dataFeature = dataset.loc[dataset['Date'] == date][features[i]]
            sp[i].plot(time[Y > 0.5],dataFeature[Y > 0.5],'r.')
            sp[i].plot(time[Y <= 0.5],dataFeature[Y <= 0.5],'b.')
            sp[i].plot(time[YEst > 0.5], YEst[YEst > 0.5]*0,'m.')
            sp[i].plot(time[YEst <= 0.5], YEst[YEst <= 0.5]*0,'y.')
            sp[i].grid(True)
            sp[i].set_xlabel('GPS Time')
            sp[i].set_ylabel(features[i])
            sp[i].legend(['Scin.','No Scin.','Est Scin.','Est no Scin.'],bbox_to_anchor=(1, 0.5),loc='center left')
        plt.savefig('figures/'+title+'.jpg')
        plt.show()