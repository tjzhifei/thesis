import numpy
import math
from monitor.classifiers.lib.online_text_svm import OnlineTextSVM

class Boosting(object):
    
    def __init__(self, n_models):
        self.n_models   = n_models
        self.clf        = list()
        self.w          = None
        self.alpha      = numpy.matrix(numpy.zeros((self.n_models, 1)))
        self.eps        = numpy.matrix(numpy.zeros((self.n_models, 1)))
    
    def get_classifier(self):
        return OnlineTextSVM(randomize = False)
    
    def predict(self, story):
        '''return the prediction from the current set of models'''
        predictions = numpy.matrix(numpy.ones((self.n_models, 1)))
        for i in xrange(0, self.n_models):
            predictions[i] = self.clf[i].predict(story)
        return numpy.sign(predictions.transpose() * self.alpha)
    
    def fit(self, stories, labels):
        '''fit all the models to the first input samples'''
        n_samples = len(stories)
        self.w = (1.0 / n_samples) * numpy.matrix(numpy.ones(n_samples))
        for i in xrange(0, self.n_models):
            clf = self.get_classifier()
            clf.fit(stories, labels, sample_weight = numpy.array(self.w[-1, :])[0])
            predictions = clf.predict(stories).reshape((n_samples, 1))
            I = numpy.matrix(map(lambda f: int(f), (predictions.transpose() != labels)[0]))
            self.eps[i] = (self.w[-1, :] * I.transpose()) / self.w[-1, :].sum(1)
            if self.eps[i] == 0:
                self.alpha[i] = 1
            else:
                self.alpha[i] = math.log((1 - self.eps[i]) / self.eps[i])
            self.w = numpy.vstack((self.w, numpy.multiply(self.w[-1, :], numpy.exp(self.alpha[i] * I))))
            self.clf.append(clf)
    
    def add(self, story, label):
        '''update all the models with the current sample, and update the alpha values'''
        n_samples = float('inf')
        for i in xrange(0, self.n_models):
            self.clf[i].add(story, label)
            if self.clf[i].get_sv_count() < n_samples:
                n_samples = self.clf[i].get_sv_count()
        self.w = (1.0 / n_samples) * numpy.matrix(numpy.ones(n_samples))
        for i in xrange(0, self.n_models):
            labels, stories = self.clf[i].support_vectors_y, self.clf[i].support_vectors_x
            predictions = numpy.zeros((self.clf[i].get_sv_count(), 1))
            for j in xrange(0, len(labels)):
                predictions[j] = self.clf[i].predict(stories[j])
            I = numpy.matrix(map(lambda f: int(f), (predictions.transpose() != labels)[0]))
            self.eps[i] = (self.w[-1, :] * I.transpose()) / self.w[-1, :].sum(1)
            if self.eps[i] == 0:
                self.alpha[i] = 1
            else:
                self.alpha[i] = math.log((1 - self.eps[i]) / self.eps[i])
            self.w = numpy.vstack((self.w[-1, :], numpy.multiply(self.w[-1, :], numpy.exp(self.alpha[i] * I))))
