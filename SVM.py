import pickle
import copy

import numpy as np
from collections import Counter
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix

def dirty_SVM_predict_free_pizza():
    pass

def train_svm_on_emails(emails, labels):
    dictionary = make_Dictionary(emails)
    train_matrix = extract_features(emails, dictionary)

    model = LinearSVC()
    model.fit(train_matrix, labels)

    result = model.predict(train_matrix)
    pickle.dump(model, open("text_classifier.pkl","wb"))

    print(confusion_matrix(train_matrix, result))


def make_Dictionary(emails):
    all_words = []
    for email in emails:
        words = email.split()
        all_words += words

    dictionary = Counter(all_words)
    #list_to_remove = copy.deepcopy(dictionary.keys())
    #for item in list_to_remove:
    #    if item.isalpha() == False:
    #        del dictionary[item]
    #    elif len(item) == 1:
    #        del dictionary[item]
    dictionary = dictionary.most_common(3000)
    return dictionary

def extract_features(emails, dictionary):
    features_matrix = np.zeros((len(emails), 3000))
    docID = 0
    for email in emails:
        words = email.split()
        for word in words:
            wordID = 0
            for i,d in enumerate(dictionary):
                if d[0] == word:
                    wordID = i
                    features_matrix[docID, wordID] = words.count(word)
        docID = docID + 1
    return features_matrix