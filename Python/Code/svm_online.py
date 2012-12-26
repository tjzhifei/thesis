#! /usr/bin/env python

import sys

from lib.util import get_comments_data
from lib.online_text_svm import OnlineTextSVM

def main(filename):
    # initial setup
    labels, _, comments = get_comments_data(filename)
    clf = OnlineTextSVM(randomize = False)
    total, correct = 0.0, 0.0

    # input first two samples (having different labels), and then continue with the online mode
    positive, negative = labels.index(1), labels.index(-1)
    clf.fit( [comments[positive], comments[negative]], [labels[positive], labels[negative]] )
    indices = [i for i in xrange(0, len(labels)) if i not in [positive, negative]]
    for i in indices:
        prediction = clf.predict(comments[i])
        clf.add(comments[i], labels[i])
        if prediction == labels[i]:
            correct = correct + 1
        total = total + 1
        print "#%d \t (label, predicted, accuracy) = (%d, %d, %.3f)" % (i, prediction, labels[i], correct * 100 / total)

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except:
        print "Usage: python %s <training_file>" % sys.argv[0]
    else:
        main(filename)