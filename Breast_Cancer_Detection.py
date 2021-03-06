#importing libraries
import numpy as np
import pandas as pd
import matplotlib 
import matplotlib.pyplot as plt
import seaborn as sns

#Loading data sets off of data
from google.colab import files
uploaded = files.upload()
df = pd.read_csv("data.csv")
df.head(7)

#count number of rows and columns in the data set
df.shape

#count number of empty(NaN, NaN, na) values in each column
df.isna().sum()

df = df.dropna(axis=1)

#Get the new count of the number of rows and columns
df.shape

#Get a count of the number of Maligant(M)[They have cancer] or Benign (B)[They don't have cancer] cells
df['diagnosis'].value_counts()

#Visualization of the count Blue for M and Orange is for B patients
sns.countplot(df['diagnosis'],label= 'count')

#Look at the data types to see which columns need to be encoded
df.dtypes

#Encode the categorial data values
from sklearn.preprocessing import LabelEncoder
labelencoder_Y= LabelEncoder()
df.iloc[:,1] = labelencoder_Y.fit_transform(df.iloc[:,1].values)

#df.iloc[:,1]

#Create a pair plot
sns.pairplot(df.iloc[:,1:6], hue='diagnosis')

#print the first 5 rows of the new data
df.head(5)

#Get the correlation of the columns
df.iloc[:,1:12].corr()

#Visualize the correlation
plt.figure(figsize=(10,10))
sns.heatmap(df.iloc[:,1:12].corr(), annot=True, fmt =".0%")

#Split the data sets into independent (x) and dependent (Y) data sets
X = df.iloc[:,2:31].values
Y = df.iloc[:,1].values
#df is a pandas.core.frame.DataFrame
#X and Y are of numpy.ndarray 
#type(X)

#We will split the data into 75% training and 25% tested, that 75% of our model training will test the remaining 25% who are supposed to be tested
from sklearn.model_selection import train_test_split
#X_train is for training and X_test is for tested and Y co-relates with it
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.25, random_state= 0)

#Scale the data (Feature_Scaling)
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.fit_transform(X_test)

#Check once X_train

#Creating a function to detect cancer for the models
def models (X_train, Y_train):

  #Logistic Regression and Use a library
  from sklearn.linear_model import LogisticRegression
  log = LogisticRegression(random_state = 0)
  log.fit(X_train, Y_train)

  #Decission Tree
  from sklearn.tree import DecisionTreeClassifier
  tree = DecisionTreeClassifier(criterion = 'entropy' , random_state = 0)
  tree.fit(X_train, Y_train)

  #Random Forest Classifier
  from sklearn.ensemble import RandomForestClassifier
  forest = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
  forest.fit(X_train, Y_train)
   
  #Printing the models accuracy on the training data
  print('[0]Logistic Regression Training Accuracy: ', log.score(X_train, Y_train))
  print('[1]Decission Tree Classifier Accuracy: ', tree.score(X_train, Y_train))
  print('[2]Random Forest Classifier Training Accuracy: ', forest.score(X_train, Y_train))

  #Returning of models
  return log,  tree, forest

#Getting all of the models
model = models(X_train, Y_train)

#Test model accuracy on test data on confusion matrix 
from sklearn.metrics import confusion_matrix


#Confusion matrix shows the true (positive and negatives values) and false (positive and negative values)
#Given below the output shows 86 as true positive ,50 is the true negative and 3 is the false positive and 4 is the false negative
for i in range( len(model) ):
  print('Model', i)
  cm  = confusion_matrix(Y_test, model[i].predict(X_test))
  
  TP = cm[0][0]
  TN = cm[1][1]
  FN = cm[1][0]
  FP = cm[0][1]
  
  print(cm)
  print("Testing Accuracy = ", (TP+TN)/(TP+TN+FN+FP))
  print( )


#Showing another way to get metrics of the models
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

for i in range( len(model) ):
  print('Model', i)
  print(classification_report(Y_test, model[i].predict(X_test)))
  print(accuracy_score(Y_test, model[i].predict(X_test)))
  print()

#Print the prediction of the Random Forest Classifier Model
pred = model[2].predict(X_test)
#This will basically predict whether or not the patient has cancer or doesn't have cancer 
print(pred)
print()
print(Y_test)
#First array is the prediction of having cancer or not 
#Second array is the actual analysis of patients having cancer
