import pandas as pd
import numpy as np

class Univariate():
     
    def quanqual(dataset):
        
        quan=[]
        qual=[]
        
        for col in dataset.columns:
            if(dataset[col].dtypes == "O"):
                qual.append(col)
            else:
                quan.append(col)
        return quan,qual
    
    
    def Univariate(quan,dataset,descriptive):

        for col in quan:
            descriptive[col]["Mean"] = dataset[col].mean()
            descriptive[col]["Median"] = dataset[col].median()
            descriptive[col]["Mode"] = dataset[col].mode()[0]
            #descriptive[col]["Q1:25%"] = np.percentile(dataset[col],25)
            #descriptive[col]["Q2:50%"] = np.percentile(dataset[col],50)
            #descriptive[col]["Q3:75%"] = np.percentile(dataset[col],75)
            #descriptive[col]["Q4:100%"] = np.percentile(dataset[col],100)
            #descriptive[col]["99%"] = np.percentile(dataset[col],99)
            descriptive[col]["Q1:25%"] = dataset.describe()[col]['25%']
            descriptive[col]["Q2:50%"] = dataset.describe()[col]['50%']
            descriptive[col]["Q3:75%"] = dataset.describe()[col]['75%']
            descriptive[col]["99%"] = np.percentile(dataset[col],99)
            descriptive[col]["Q4:100%"] = dataset.describe()[col]['max']
            descriptive[col]["IQR"] = descriptive[col]["Q3:75%"] - descriptive[col]["Q1:25%"]
            descriptive[col]["1.5Rule"] = 1.5 * descriptive[col]["IQR"]
            descriptive[col]["Lesser"] = descriptive[col]["Q1:25%"] - descriptive[col]["1.5Rule"]
            descriptive[col]["Greater"] = descriptive[col]["Q3:75%"] + descriptive[col]["1.5Rule"]
            descriptive[col]["Min"] = dataset[col].min()
            descriptive[col]["Max"] = dataset[col].max()
        return descriptive
    
    def freqtable(col,dataset):
        freqtable = pd.DataFrame(columns=["Unique_Values","Frequency","Relative_Frequency","Cumsum"])
        freqtable["Unique_Values"]=dataset[col].value_counts().index
        freqtable["Frequency"]=dataset[col].value_counts().values
        freqtable["Relative_Frequency"]=freqtable["Frequency"]/103
        freqtable["Cumsum"]=freqtable["Relative_Frequency"].cumsum()
        return freqtable
    
    def IdentifyOutlier(quan,descriptive):
    
        Lesser=[]
        Greater=[]

        for col in quan:
            if (descriptive[col]['Min']<descriptive[col]['Lesser']):
                Lesser.append(col)
            if (descriptive[col]['Max']>descriptive[col]['Greater']):
                Greater.append(col)
        return Lesser, Greater
    
    def ReplaceOutlier(dataset,Lesser,Greater,descriptive):
        
        for col in Lesser:
            dataset[col][dataset[col]<descriptive[col]['Lesser']]=descriptive[col]['Lesser']
        for col in Greater:
            dataset[col][dataset[col]>descriptive[col]['Greater']]=descriptive[col]['Greater']