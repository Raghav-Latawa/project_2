

import nltk
import re
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import pylab as pl
nltk.download()
def preprocess(tweet):
    
  
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    
  
    tweet = re.sub('@[^\s]+','__USERHANDLE',tweet)  
    
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    
  
    tweet = tweet.strip('\'"')
    

    repeat_char = re.compile(r"(.)\1{1,}", re.IGNORECASE)
    tweet = repeat_char.sub(r"\1\1", tweet)
    
  
    emoticons = \
    [
     ('__positive__',[ ':-)', ':)', '(:', '(-:', \
                       ':-D', ':D', 'X-D', 'XD', 'xD', \
                       '<3', ':\*', ';-)', ';)', ';-D', ';D', '(;', '(-;', ] ),\
     ('__negative__', [':-(', ':(', '(:', '(-:', ':,(',\
                       ':\'(', ':"(', ':((','D:' ] ),\
    ]

    def replace_parenthesis(arr):
       return [text.replace(')', '[)}\]]').replace('(', '[({\[]') for text in arr]
    
    def join_parenthesis(arr):
        return '(' + '|'.join( arr ) + ')'

    emoticons_regex = [ (repl, re.compile(join_parenthesis(replace_parenthesis(regx))) ) \
            for (repl, regx) in emoticons ]
    
    for (repl, regx) in emoticons_regex :
        tweet = re.sub(regx, ' '+repl+' ', tweet)

  
    tweet = tweet.lower()
    
    return tweet


def stem(tweet):
        stemmer = nltk.stem.PorterStemmer()
        tweet_stem = ''
        words = [word if(word[0:2]=='__') else word.lower() \
                    for word in tweet.split() \
                    if len(word) >= 3]
        words = [stemmer.stem(w) for w in words] 
        tweet_stem = ' '.join(words)
        return tweet_stem

dataset = pd.read_csv('https://grubhub-bucket.s3.us-east-2.amazonaws.com/training.1600000.processed.noemoticon.csv', skiprows=750000, nrows=100000, encoding='ISO-8859-1',header=None)
X=dataset.iloc[:,5].values
X=pd.Series(X)
y=dataset.iloc[:,0].values
'''
for row in range(0,1600000):
    if y[row]==4:
        y[row]=1
    else:
        y[row]=0
'''

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.20, random_state=5)

X_train = [stem(preprocess(tweet)) for tweet in X_train]
X_test = [stem(preprocess(tweet)) for tweet in X_test]

vec = TfidfVectorizer(min_df=5, max_df=0.95, sublinear_tf = True,use_idf = True,ngram_range=(1, 2))
X_train_vec = vec.fit_transform(X_train)
X_test_vec = vec.transform(X_test)
#nb = MultinomialNB()

from sklearn.svm import SVC
svclassifier = SVC(kernel = 'linear')
svclassifier.fit(X_train_vec, y_train)

import pickle

pickle.dump(svclassifier, open("SVMModel", 'wb'))

import pickle
svmLoaded = pickle.load(open('/content/SVMModel', 'rb'))

testData = pd.read_csv('/content/test_labelled.csv')
# testData = testData[pd.notnull(testData['sentiment'])]
print(testData.shape[0])
del testData['location']
# testData = testData.dropna()
testData = testData[pd.notnull(testData['sentiment'])]
print(testData.shape[0])

y_test_new = testData['sentiment']
tweetsTestData = testData['text']

tweetsTestData = [stem(preprocess(tweet)) for tweet in tweetsTestData]

X_test_vec_new = vec.transform(tweetsTestData)
print(y_test_new)

log_predicted= svmLoaded.predict(X_test_vec_new)

logreg_score = round(svmLoaded.score(X_train_vec, y_train) * 100, 2)
logreg_score_test = round(svmLoaded.score(X_test_vec_new, y_test_new) * 100, 2)

print('Logistic Regression Training Score: \n', logreg_score)
print('Logistic Regression Test Score: \n', logreg_score_test)
print('Coefficient: \n', svmLoaded.coef_)
print('Intercept: \n', svmLoaded.intercept_)
print('Accuracy: \n', metrics.accuracy_score(y_test_new,log_predicted))
print('Confusion Matrix: \n', metrics.confusion_matrix(y_test_new,log_predicted))
print('Classification Report: \n', metrics.classification_report(y_test,log_predicted))

