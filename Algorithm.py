# Class: Algorithm
# Usage: storage and operation of information about algorithm
#
# Methods: 
#           void fit(X: List, Y: List)
#           YEst: List void predict(X: List) 


from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import SGDClassifier
import numpy as np

class Algorithm(object):
    # Initialize the chosen algorithm with parameters set by user
    def __init__(self, algorithm = 'decision tree', parameters = {}):  # algorithm: String, Parameters: Dict {paramName:paramValue}
        
        self.algorithm = algorithm
        if self.algorithm == 'decision tree':               # needed parameter: max_depth
            if parameters == {}:
                self.classifier = DecisionTreeClassifier(max_depth = 2)
            else:
                self.classifier = DecisionTreeClassifier(max_depth = parameters['max_depth'])
        elif self.algorithm == 'support vector machine':    # needed parameters: penalty, tol, C, class_weight              # needed parameter: max_depth
            if parameters == {}:
                self.classifier = LinearSVC(dual=False, penalty='l1', tol=0.00001, C=1.0, class_weight=None)
            else:
                self.classifier = LinearSVC(dual = False, penalty = parameters['penalty'], tol = parameters['tol'], C = parameters['C'], class_weight = parameters['class_weight'])
        elif self.algorithm == 'random forest':             # needed parameters: n_estimators, max_features, min_samples_leaf, max_depth              # needed parameter: max_depth
            if parameters == {}:
                self.classifier = RandomForestClassifier(n_estimators=20, max_features='auto', min_samples_leaf=3, max_depth=3)
            else:
                self.classifier = RandomForestClassifier(n_estimators = parameters['n_estimators'], max_features = parameters['max_features'], min_samples_leaf = parameters['min_samples_leaf'], max_depth = parameters['max_depth'])
        elif self.algorithm == 'adaboost':                  # needed parameters: base_estimator, n_estimators, learning_rate, algorithm.
            print 'adaboost start'
            if parameters == {}:
                self.classifier = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=2), n_estimators=60,learning_rate=1,algorithm='SAMME')
            else:
                print 'cls1 '+parameters['base_estimator']
                if parameters['base_estimator'] == 'decision tree':
                    baseEstimator = DecisionTreeClassifier(max_depth = 2)
                elif parameters['base_estimator'] == 'support vector machine':
                    baseEstimator = LinearSVC(dual=False, penalty='l1', tol=0.00001, C=1.0, class_weight=None)
                elif parameters['base_estimator'] == 'random forest':
                    baseEstimator = RandomForestClassifier(n_estimators=20, max_features='auto', min_samples_leaf=3, max_depth=3)
                else:
                    print 'cls2 '+parameters['base_estimator']
                self.classifier = AdaBoostClassifier(base_estimator = baseEstimator, n_estimators = parameters['n_estimators'], learning_rate = parameters['learning_rate'],algorithm = parameters['algorithm'])

    def getAlgorithm(self):
        return self.algorithm

    def getParameters(self):
        return self.classifier.get_params()

    def fit(self, X, Y):
        self.classifier.fit(X,Y)

    def predict(self, X):
        return self.classifier.predict(X)

    def aggregation(self, Y, maxGap):
        loc1_1 = 0
        for i in range(len(Y)-maxGap):
            if Y[i] > 0.5:
                loc1_2 = loc1_1
                loc1_1 = i
                if 1.5 < loc1_1-loc1_2 < maxGap:
                    for iter in range(loc1_2+1,loc1_1):
                        Y[iter] = 1