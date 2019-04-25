from __future__ import print_function, division
from future.utils import iteritems
from builtins import range
import nltk
import csv
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.utils import shuffle
from nltk.stem import WordNetLemmatizer
from sklearn.linear_model import LogisticRegression
import pandas as pd
import re
import matplotlib.pyplot as plt


wordnet_lemmatizer = WordNetLemmatizer()
stopwords = set(w.rstrip() for w in open('stopwords.txt'))

positive_reviews=pd.read_csv("Train_Positive.csv")
positive_reviews=positive_reviews["reviewText"]

negative_reviews=pd.read_csv("Train_Negative.csv")
negative_reviews=negative_reviews["reviewText"]


total_num_of_reviews = len(positive_reviews) + len(negative_reviews)

# nltk.tokenize.word_tokenize(t.text) does tokenization but cannot differentiate between the same words in lowercase and uppercase.
# so necessary to  convert string to lower and then lemmatize

def my_tokenizer(s):
    pattern = r'[^a-zA-Z\s]'
    s = re.sub(pattern,'',s)
    s = s.lower() # downcase to make no difference between Upper and LowerCase.

    tokens = nltk.tokenize.word_tokenize(s) # split string into words (tokens).

    tokens = [t for t in tokens if len(t) > 2] # remove short words like to, hi etc.

    tokens = [wordnet_lemmatizer.lemmatize(t) for t in tokens] # put words into base form instead of using a Stemmer

    tokens = [t for t in tokens if t not in stopwords] # remove stopwords by checking them from the txt file.
    
    return tokens


word_index_map = {} # map word to an index  

current_index = 0

positive_tokenized = [] # array to store +ve words

negative_tokenized = [] # array to store -ve words

orig_reviews = [] # array that stores our original reviews

test_tokenized = []



for review in positive_reviews:

    orig_reviews.append(review)

    tokens = my_tokenizer(review) # split sentence into tokens

    positive_tokenized.append(tokens)  # append 

    for token in tokens:

        if token not in word_index_map:

            word_index_map[token] = current_index

            current_index += 1


for review in negative_reviews:

    orig_reviews.append(review)

    tokens = my_tokenizer(review)

    negative_tokenized.append(tokens)

    for token in tokens:

        if token not in word_index_map:

            word_index_map[token] = current_index

            current_index += 1
 
print("len(word_index_map):", len(word_index_map)) # total number of unique words found in the reviews.

def tokens_to_vector(tokens, label):

    x = np.zeros(len(word_index_map) + 1) # fill a numpy array with zeroes for each token in word map

    for t in tokens:

        i = word_index_map[t] # get its index

        x[i] += 1

        x=x/x.sum() # normalize it before setting label

    x[-1] = label 

    return x

N = len(positive_tokenized) + len(negative_tokenized)


data = np.zeros((N, len(word_index_map) + 1))

i = 0
for tokens in positive_tokenized:

    xy = tokens_to_vector(tokens, 1)

    data[i,:] = xy

    i += 1

for tokens in negative_tokenized:

    xy = tokens_to_vector(tokens, 0)

    data[i,:] = xy

    i += 1

orig_reviews, data = shuffle(orig_reviews, data)

X = data[:, :-1]
Y = data[:, -1]

# last 1000 rows will be test

Xtrain = X[:-6200,]

Ytrain = Y[:-6200,]

Xtest = X[-1000:,]

Ytest = Y[-1000:,]

model = LogisticRegression(solver ='lbfgs')
model.fit(Xtrain, Ytrain)
print("Train accuracy:", round(model.score(Xtrain, Ytrain),4))
print("Test accuracy:", round(model.score(Xtest, Ytest),4))

threshold = 0.5
#for word, index in iteritems(word_index_map):

  #  weight = model.coef_[0][index]

 #   if weight > threshold or weight < -threshold:

#        print(word, weight)
#predict probabilities

predictions = model.predict(Xtest)
P = model.predict_proba(Xtest)[:,1] # p(y = 1 | x)

def createPlots(positive,negative):
    #PosChart
    labels = 'PositiveReviews', 'NegativeReviews'
    sizes = [positive,negative]
    colors = ['red', 'lightskyblue']
    explode = (0.2,0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()

def writeToCSV(P):
    pos = open("positiveReview.csv",'w')
    neg = open("negativeReview.csv",'w')
    Poswriter = csv.writer(pos)
    Poswriter.writerow(['SerialNo','Review','PredictedProbability'])
    positive = 0
    Negwriter = csv.writer(neg)	
    Negwriter.writerow(['SerialNo','Review','PredictedProbability'])
    negative = 0
    i=0;
    for review in orig_reviews[-1000:]:   
        if(P[i]>=0.5):
            positive=positive+1
            Poswriter.writerow([positive,review,round(P[i],3)])
        else:
            negative=negative+1
            Negwriter.writerow([negative,review,round(P[i],3)])
        i=i+1	
    pos.close()
    neg.close()
    createPlots(positive,negative)

writeToCSV(P)

