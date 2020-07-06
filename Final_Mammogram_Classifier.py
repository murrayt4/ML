from __future__ import division
import os#for changin directory
from math import log#for working with logartihms
import numpy as np#import Numbpy library
import pandas as pd#import Panda Library
import operator#For changing directory
cwd = os.getcwd()#Shows current directory
os.chdir("/BMED Elec and Inst")#Changes directory to personal location where Excel File is located
cwd = os.getcwd()
Excel_file = ('Mammography Classifer Data.xlsx')#Sets file name to variable
newfile = pd.ExcelFile(Excel_file, sheetname = 0, index_col = 0)#Opens Excel file
df = newfile.parse(0)#Assigns sheet 1 to df
MassMargin  = [newfile.parse(2),newfile.parse(3),newfile.parse(4),newfile.parse(5), newfile.parse(6)]#Sets all Mass Margin excel sheets to variable Mass Margin
MassShape = [newfile.parse(8),newfile.parse(9),newfile.parse(10),newfile.parse(11)]#Sets all Mass Shape excel sheets to variable Mass Shape
MassDensity = [newfile.parse(13),newfile.parse(14),newfile.parse(15),newfile.parse(16)]#Sets all Mass Density excel sheets to variable Mass Density
Age = [newfile.parse(18),newfile.parse(19),newfile.parse(20),newfile.parse(21)]#Sets all Age excel sheets to variable Age
MassMargin = [MassMargin[0]['Severity'],MassMargin[1]['Severity'],MassMargin[2]['Severity'],MassMargin[3]['Severity'],MassMargin[4]['Severity']]#Assigns only Severity results column to variables
MassShape = [MassShape[0]['Severity'],MassShape[1]['Severity'],MassShape[2]['Severity'],MassShape[3]['Severity']]
MassDensity = [MassDensity[0]['Severity'],MassDensity[1]['Severity'],MassDensity[2]['Severity'],MassDensity[3]['Severity']]
Age = [Age[0]['Severity'],Age[1]['Severity'],Age[2]['Severity'],Age[3]['Severity']]
Severity = df['Severity']
Title = ('Mass Margin', 'Mass Shape', 'Mass Density', 'Age', 'Severity')
MMTitle = ('Circumscribed', 'Mircolobulated', 'Obscured','Ill-Defined', 'Spiculated')
MSTitle = ('Round', 'Oval', 'Lobular', 'Irregular')
MDTitle = ('High', 'Iso', 'Low', 'Fat-Containing')
AgeTitle = ('18-38', '36-56', '57-74', '74-96')
SeverityTitle = ('Benign', 'Malignent')
Dat = [MassMargin,MassShape,MassDensity,Age]
tree = []
Mem = []
re = {'First':[],'Second':[],'Third':[],'Fourth':[]}
count = 0
numb = []

#Legend	
#Age 18-38	1
#Age 38-56	2
#Age 57-74	3
#Age 74-	4
#If severity == 1, Malignent Tumor (Positive)
#If severity == 0, Benign Tumor (Negative)

######### This function counts number of Malignent and Benign Tumors###########
#Parameters:
#Data - a set of severity values
def partition(Data):
    P = 0#Counter for Positive values
    N = 0#Counter for Negative values
    for i in range(len(Data)):#Loops through every value in Data
        if(Data[i] > 0):
            P += 1#if Severity == 1, increases count of positive
        else:
            N += 1#if Severity == 0, increase count of negative
    return P,N

def percent(Data):
    P,N = partition(Data)
    Mal = P / (P + N)
    Benign = N / (P + N)
    return Mal, Benign
    
######### This function calcuates the entropy (randomness) of a dataset ########
#Parameters:
#Data - a set of severity values
def calcentropy(Data): 
    Positive,Negative = partition(Data)#Calls partition Data function
    sum1 = Positive + Negative#Total number of values
    if len(Data) == 0:#If there is no data, return 0 entropy
        return 0
    ratio = Positive / (sum1)#Ratio of positive results
    ratio2 = Negative / (sum1)#Ratio of Negative results
    if ratio == 0 or ratio2 == 0:
        return 0
    else:#Calculates Entropy
        first = - ratio * log(ratio,2)
        second = ratio2 * log(ratio2, 2)
        entropy = first - second
    return entropy

######## Calcuates information gain (how much entropy is reduced) of a inputted feature ############
#Parameters:
#Feature - a dataset of severities of specific feature (either MassMargin,MassShape,MassDensity, or Age)
#Severity - dataset of severity of entire dataset
def gain(Feature,Severity):# gain function, ADD A WAY TO RETURN GAIN OF 0
    counter = 0
    for i in range(0,4):
        if len(Feature[i]) == 0:#Loops through the length of each Feature class to check that dataset is not empty 
            counter +=1
    if counter == 4:
        return -1#Returns a -1 if dataset is empty(already used)
    Sum = [0,0,0,0,0]
    num = 0
    count = -1
    for i in Feature:
        count += 1
        for j in Feature[count]:#Loops through each sheet and stores sum of values in sum array
            Sum[count]+= 1
    TotalValue = len(Severity)#Total number of values 
    Entropies = [0,0,0,0,0]
    count = -1
    for i in Feature:
        count += 1
        Entropies[count] += calcentropy(Feature[count])#Computs entropy for each feature and stores it in entropies array
    IG = 0
    partial = 0
    count = -1
    for i in Feature:
        count += 1
        partial += ((Sum[count] / TotalValue) * (Entropies[count]))
    IG = calcentropy(Severity) - partial
    return IG
    
def choose(data, Seve):
    features = len(list(data))#Stores number of features invariable
    bestInfoGain = 0#Creates info gain variable
    bestFeat = None
    i = 0
    while i < features:#For every variable in features
        featList = list(data)
        infoGain = gain(data[i], Seve)
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain#If calculated infogain is better then current infogain, set as new
            bestFeat = i#Make this feature the best feature
        i +=1
    return bestInfoGain, bestFeat

def majorityvalue(Severity):
    if not Severity:
        pass
    else:
        P,N = partition(Severity)
        if P/N >= 1:
            return 1
        else:
            return 0
    
def split(Data,BestInfoGain,Class,Mem):
    if len(Mem) > 4:
        Mem = []
    i = 0
    count = 0
    BigData = []
    newData = []
    Attribute = 0
    features = len(list(Data))   
    while i < features:#For every variable in features
        featList = list(Data)
        
        infoGain = gain(Data[i],Class)#Computes infogain for each attribute
        if(infoGain == BestInfoGain):#Finds which Attribute is BestInfoGain
            Attribute = i#Attribute is integer value refering to attribute index
            break
        i +=1
    Mem.append(Attribute)
    if Attribute == 0:
        if len(Mem) == 2:
            rem = re['First']
            for j in range(1,6):
                for i in df[Title[Attribute]]:#refecenes attribute index         
                    if df.iloc[count,Attribute] == j and df.iloc[count,Mem[0]] == rem:#if that specific row is equal to branch
                        newData.append(df.iloc[count,:])#add that row to new data
                    count += 1
                count = 0
                BigData.append(newData)
                newData = []
        elif len(Mem) == 3:
            rem = re['First']
            r = re['Second']
            for j in range(1,6):
                for i in df[Title[Attribute]]:#refecenes attribute index         
                    if df.iloc[count,Attribute] == j and df.iloc[count,Mem[0]] == rem and df.iloc[count,Mem[1]] == r:#if that specific row is equal to branch
                        newData.append(df.iloc[count,:])#add that row to new data
                    count += 1
                count = 0
                BigData.append(newData)
                newData = []
        elif len(Mem) == 4:
            rem = re['First']
            r = re['Second']
            rr = re['Third']
            for j in range(1,6):
                for i in df[Title[Attribute]]:#refecenes attribute index         
                    if df.iloc[count,Attribute] == j and df.iloc[count,Mem[0]] == rem and df.iloc[count,Mem[1]] == r and df.iloc[count,Mem[2]] == rr:#if that specific row is equal to branch
                        newData.append(df.iloc[count,:])#add that row to new data
                    count += 1
                count = 0
                BigData.append(newData)
                newData = []
        else:
            for j in range(1,6):
                for i in df[Title[Attribute]]:#refecenes attribute index
                    if df.iloc[count,Attribute] == j:#if that specific row is equal to branch
                        newData.append(df.iloc[count,:])#add that row to new data
                    count += 1
                count = 0
                BigData.append(newData)
                newData = []
    else:#If Mass Shape or Mass Density is selected Attribute
        if len(Mem) == 2:
            rem = re['First']
            for j in range(1,5):
                for i in df[Title[Attribute]]:#refecenes attribute index         
                    if df.iloc[count,Attribute] == j and df.iloc[count,Mem[0]] == rem:#if that specific row is equal to branch
                        newData.append(df.iloc[count,:])#add that row to new data
                    count += 1
                count = 0
                BigData.append(newData)
                newData = []
        elif len(Mem) == 3:
            rem = re['First']
            r = re['Second']
            for j in range(1,5):
                for i in df[Title[Attribute]]:#refecenes attribute index         
                    if df.iloc[count,Attribute] == j and df.iloc[count,Mem[1]] == r and df.iloc[count,Mem[0]] == rem:#if that specific row is equal to branch
                        newData.append(df.iloc[count,:])#add that row to new data
                    count += 1
                count = 0
                BigData.append(newData)
                newData = []
        elif len(Mem) == 4:
            rem = re['First']
            r = re['Second']
            rr = re['Third']
            for j in range(1,5):
                for i in df[Title[Attribute]]:#refecenes attribute index         
                    if df.iloc[count,Attribute] == j and df.iloc[count,Mem[0]] == rem and df.iloc[count,Mem[1]] == r and df.iloc[count,Mem[2]] == rr:#if that specific row is equal to branch
                        newData.append(df.iloc[count,:])#add that row to new data
                    count += 1
                count = 0
                BigData.append(newData)
                newData = []
        else:
            for j in range(1,5): 
                for i in df[Title[Attribute]]:#refecenes attribute index
                    if df.iloc[count,Attribute] == j:#if that specific row is equal to branch
                        newData.append(df.iloc[count,:])#add that row to new data
                    count += 1
                count = 0
                BigData.append(newData)
                newData = []
    return BigData, Attribute,Mem

def printFeature(BestFeat,MM,MS,MD,AGE):
    if BestFeat == None:
        return
    elif BestFeat == 0:
        print("What is",Title[BestFeat],"?")
        print("--> ",MMTitle[MM])
    elif BestFeat == 1:
        print("What is",Title[BestFeat],"?")
        print("--> ",MSTitle[MS])
    elif BestFeat == 2:
        print("What is",Title[BestFeat],"?")
        print("--> ",MDTitle[MD])
    else:
        print("What is",Title[BestFeat],"?")
        print("--> ",AgeTitle[AGE])

def printSeverity(Severity,val):
    if val == 0:
        if Severity == 1:
            print("100% of tumors in the patient database were classified as malignent")
        else:
            print("100% of tumors in the patient database were classified as benign")
    elif val == 1:
        Mal,Benign = percent(Severity)
        if majorityvalue(Severity) == 1:
            print("%.2f" % round(Mal,2), "% of similiar tumors in the patient datbase were classified as malignent")
        else:
            print("%.2f" % round(Benign,2),"% of similiar tumors in the patient database were classified as benign")
            
    #########TestTree Function######################
#######Predict's Severity of Patient Tumor ################
def TestTree(Da,Class,Mem,MM,MS,MD,Age,OldClass):
    val = -1
    BestGain,BestFeat = choose(Da,Class)
    NewData,Attri,Mem = split(Da,BestGain,Class,Mem)
    if BestFeat == None:
        if not Class:
            val = 1
            printSeverity(OldClass,val)#Base Case 1
            return majorityvalue(OldClass)
        else:
            val = 1
            printSeverity(Class,val)
            return majorityvalue(Class)#Base Case 2
    OldClass = Class
    if Attri == 0:
        printFeature(BestFeat,MM,MS,MD,Age)
        Data,Severity = process(NewData[MM],Mem)
        if len(set(Severity)) == 1:
            val = 0
            printSeverity(Severity[0],val)
            return Severity[0]#Base Case 3
        else:
            return TestTree(Data,Severity,Mem,MM,MS,MD,Age,OldClass)#Recursive Call
    elif Attri == 1:
        printFeature(BestFeat,MM,MS,MD,Age)
        Data,Severity = process(NewData[MS],Mem)
        if len(set(Severity)) == 1:
            val = 0
            printSeverity(Severity[0],val)
            return Severity[0]#Base Case 3
        else:
            return TestTree(Data,Severity,Mem,MM,MS,MD,Age,OldClass)
    elif Attri == 2:
        printFeature(BestFeat,MM,MS,MD,Age)
        Data,Severity = process(NewData[MD],Mem)
        if len(set(Severity)) == 1:
            val = 0
            printSeverity(Severity[0],val)
            return Severity[0]#Base Case 3
        else:
            return TestTree(Data,Severity,Mem,MM,MS,MD,Age,OldClass)
    elif Attri == 3:
        printFeature(BestFeat,MM,MS,MD,Age)
        Data,Severity = process(NewData[Age],Mem)
        if len(set(Severity)) == 1:
            val = 0
            printSeverity(Severity[0],val)
            return Severity[0]#Base Case 3
        else:
            return TestTree(Data,Severity,Mem,MM,MS,MD,Age,OldClass)
        

def process(Vals,Mem): #This returns an array of [Margin,Shape,Density,Age] for a given child Attribute(ex. Circumulated).
    e = [[],[],[],[]]
    for num in range(0,4):
        for p in Vals:
           e[num].append(p[num])
    for num in range(0,4):
        e[num] = set(e[num])
        if len(e[num]) == 1:
            if num not in numb:
                numb.append(num)
                number = e[num].pop()
                if  len(re['First']) == 0: 
                    re['First'].append(number)
                elif len(re['First']) == 1 and len(re['Second']) == 0 and len(re['Third']) == 0 and len(re['Fourth']) == 0:# and num not in numb:
                    re['Second'].append(number)
                elif len(re['First']) == 1 and len(re['Second']) == 1 and len(re['Third']) == 0 and len(re['Fourth']) == 0:# and num not in numb:
                    re['Third'].append(number)
                elif len(re['First']) == 1 and len(re['Second']) == 1 and len(re['Third']) == 1 and len(re['Fourth']) == 0:# and num not in numb:
                    re['Fourth'].append(number)
                elif len(re['First']) == 1 and len(re['Second']) == 1 and len(re['Third']) == 1 and len(re['Fourth']) == 1:# and num not in numb:
                    pass
    
    Sever = []
    Array = [0,0,0,0]
    Margin = [[],[],[],[],[]]
    Shape = [[],[],[],[]]
    Density = [[],[],[],[]]
    Age = [[],[],[],[]]
    for p in Vals:#Searches through every value in inputted attribute
        for i in range(0,4):
            if(i == 0):#Specifies first column, Mass Margin
                for va in Mem:
                    if va == i:
                        break
                else:
                    if p[i] == 1: 
                        Margin[0].append(p[4])#Adds Mass Margin type 1 to Shape array
                    elif p[i] == 2:
                        Margin[1].append(p[4])#Adds Mass Margin type 2 to Shape array
                    elif p[i] == 3:
                        Margin[2].append(p[4])#Adds Mass Margin type 3 to Shape array
                    elif p[i] == 4:
                        Margin[3].append(p[4])#Adds Mass Margin type 4 to Shape array
                    elif p[i] == 5:
                        Margin[4].append(p[4])
            if(i == 1):#Specifies first column, Mass Shape
                for va in Mem:
                    if va == i:
                        break
                else:
                    if p[i] == 1: 
                        Shape[0].append(p[4])#Adds Mass Shape type 1 to Shape array
                    elif p[i] == 2:
                        Shape[1].append(p[4])#Adds Mass Shape type 2 to Shape array
                    elif p[i] == 3:
                        Shape[2].append(p[4])#Adds Mass Shape type 3 to Shape array
                    elif p[i] == 4:
                        Shape[3].append(p[4])#Adds Mass Shape type 4 to Shape array
            if(i == 2):
                for va in Mem:
                    if va == i:
                        break
                else:
                    if p[i] == 1:      
                        Density[0].append(p[4])#Adds Mass Density type 1 to Density array
                    elif p[i] == 2:
                        Density[1].append(p[4])#Adds Mass Density type 2 to Density array
                    elif p[i] == 3:
                        Density[2].append(p[4])#Adds Mass Density type 3 to Density array
                    elif p[i] == 4:
                        Density[3].append(p[4])#Adds Mass Density type 4 to Density array
            if(i == 3):
                for va in Mem:
                    if va == i:
                        break
                else:
                    if p[i] == 1:      
                        Age[0].append(p[4])#Adds Age type 1 to Age array
                    elif p[i] == 2:
                        Age[1].append(p[4])#Adds Age type 2 to Age array
                    elif p[i] == 3:
                        Age[2].append(p[4])#Adds Age type 3 to Age array
                    elif p[i] == 4:
                        Age[3].append(p[4])#Adds Age type 4 to Age array 
    for p in Vals:
            Sever.append(p[4])
    Array = [Margin,Shape,Density,Age]#Severities of Shape, Density, and Age for a inputed Mass Margin Attribute

    return Array,Sever

#To Run Code, Input Features in the first four number slots. Leave the last number 0.
Test = TestTree(Dat,Severity,Mem,3,1,2,1,0)
print(Test)


    
