print("WELCOME TO FAKE NEWS DETECTION\n")
#Importing Libraries
#pandas is a fast, powerful, flexible and easy to use open source 
#data analysis and manipulation tool.
import pandas as pd
#Numpy is the most fundamental module for scientific computing with Python.
#Numpy provides the support of highly optimized multidimensional arrays,
#which are the most basic data structure of most Machine Learning algorithms.
import numpy as np
#Matplotlib is a plotting library for the Python programming language 
#and its numerical mathematics extension NumPy.
import matplotlib as plt
#Pickle in Python is primarily used in serializing and 
#deserializing a Python object structure.
import pickle

print("Libraries Imported Successfully !\n")

#Importing Dataset 
dataset = pd.read_csv('train.csv')
#Droping Label Column
X = dataset.drop('label',axis=1)
#Dropna is used for deleting all the N/A Values
dataset = dataset.dropna()
#Creating copy of Dataset into Messages
messages = dataset.copy()
#Reseting all the indexies in the Dataset
messages.reset_index(inplace=True)

print("Dataset Imported Successfully !\n")

print("Creating Bag of Words Model ...\n")
#Cleaning the text 
#Python's built-in “re” module provides excellent support for regular 
#expressions ,with a modern and complete regex flavor.
import re
#NLTK Module is used to work with Human Language Data
from nltk.corpus import stopwords
#NLTK Module is also use for Natural Language Processing
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
corpus = []
for i in range(0, len(messages)):
    review = re.sub('[^a-zA-Z]', ' ', messages['title'][i])
    review = review.lower()
    review = review.split()
    
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)
    corpus.append(review)


#Creating bag of words model

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=1500)
#Dividing Dataset into Independent Variable and Dependent Variable
X = cv.fit_transform(corpus).toarray()
Y = dataset.iloc[:,-1].values

# Pickle.dump function is used to save created Machine Learning Model
pickle.dump(cv, open('tranform.pkl', 'wb'))


#Splitting the data into Trainset and Testset
from sklearn.model_selection import train_test_split
#Creating Test set of size 20% of total Dataset
x_train,x_test,y_train,y_test = train_test_split(X,Y, test_size=0.2)

from sklearn.naive_bayes import GaussianNB
#A Gaussian Naive Bayes algorithm is a special type of NB algorithm. 
#It’s specifically used when the features have continuous values. 
#It’s also assumed that all the features are following a gaussian distribution i.e, normal distribution.
clf = GaussianNB()
#Fitting X-train and Y-train with GaussianNB
clf.fit(x_train,y_train)

print("Model Created Successfully !\n")

#Creating Y-pred 
y_pred = clf.predict(x_test)

#print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix \n")
print(cm)
print("\n")
print("********************")
message=input("Enter Text Here : ")
message = [message]
#X_new_counts = count_vect.transform(input.plot_movie)
data = cv.transform(message).toarray()
myprediction = clf.predict(data)
print("\n")
if myprediction==1 :
    print("Beware! It's a Fake News!!\n")
else:
    print("Good! It's a Real News!!\n")

#Calculating Accuracy of the News
accuracy = accuracy_score(y_test, y_pred)

print("The Accuracy of this Model is : ",round(accuracy, 2));

print("\n")

#1 = unreliable/ Fake 
#0 = reliable/ Not Fake

filename = 'nlp_model.pkl'
pickle.dump(clf, open(filename, 'wb'))

print("Model Executed Successful !!\n")
print("Thank You !")