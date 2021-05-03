# Load the Pandas libraries with alias 'pd'
import pandas as pd
from GeneticProgrammingLibrary import Rule, GeneticProgram
from CommonLibrary import CommonMethods
from Svm_Library import Features
from sklearn import svm
from numpy import genfromtxt, savetxt

# Creating a DataFrame for the three csv files using pandas
# When you want to read any of the files using indexes use iloc. E.g. train.iloc[0][0].
# The DataFrames work like an array of arrays (an array for each row).

# Creating a DataFrame for the "train.csv" file.
originalTrainDataset = pd.read_csv("Data/train.csv")

 #Run the genetic program for every rule.
for i in range(1, 10):
    print("Generating rules for hand classification: ", i)
    geneticProgramRule = GeneticProgram.GeneticProgram(i, 5, originalTrainDataset)
    geneticProgramRule.runProgram()
    print("End of rule generation for hand classification: ", i)
    print()
    print()


## Creating a DataFrame for the "test.csv" file.
originalTestDataset = pd.read_csv("Data/test.csv")
##############################################################################################################
#SVM Approach
#create the training & test sets, skipping the header row with [1:]
dataset = genfromtxt(open('Data/trainFeatures.csv','r'), delimiter=',', dtype='f8')[1:]    
train_tags = [x[-1] for x in dataset]
train = [x[:-1] for x in dataset]

clf_svm = svm.SVC(random_state=0,gamma=0.001,C=100).fit(train, train_tags)

predicted_svm = clf_svm.predict(train)

correct = 0
for tag, pred in zip(train_tags, predicted_svm):
    if(tag==pred):
        correct+= 1
print("Correctly classified %s total training examples out of %s examples" %(correct,len(train_tags)))
# -------------------------------------------------------------------------------------------------------
# SVM Model on test set
test_dataset = genfromtxt(open('Data/testFeatures.csv','r'), delimiter=',', dtype='f8')[1:]
test =  [x[1:-1] for x in test_dataset]
test_tags = [x[-1] for x in test_dataset]
# test = [x[:-1] for x in test_dataset]

test_predicted_svm =clf_svm.predict(test)

test_correct=0
for tag, pred in zip(test_tags, test_predicted_svm):
    if(tag==pred):
        test_correct+= 1
print("Correctly classified %s total training examples out of %s examples" %(test_correct,len(test_tags)))

geneticProgramRule.classifyHandGP(originalTestDataset, test_tags)
# Creating a DataFrame for the "sampleSubmission.csv" file.
sampleSubmission = pd.read_csv("Data/sampleSubmission.csv")