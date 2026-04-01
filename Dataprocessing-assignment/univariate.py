class Univariate():
    ## Quantitative columns and Qualitative column separation
    def QuanQual(dataset):
        Quan=[]
        Qual=[]
        for col in dataset.columns:
            if dataset[col].dtype != 'object':
                Quan.append(col)
            else:
                Qual.append(col)
        return Quan, Qual

    ## Function is creating custom describe table with values named as descriptive
    def univariate(dataset,Quan):
        import pandas as pd
        import numpy as np
        descriptive = pd.DataFrame(index=["Mean","Median","Mode","Q1:25 %","Q2:50 %","Q3:75 %","99 %","Q4:100 %","IQR","1.5Rule","Lesser","Greater","Min","Max","Skew","Kurtosis"], columns=Quan)
        for col in Quan:
            descriptive[col]["Mean"]=dataset[col].mean()
            descriptive[col]["Median"]=dataset[col].median()
            descriptive[col]["Mode"]=dataset[col].mode()[0]
            descriptive[col]["Q1:25 %"] = dataset.describe()[col]["25%"]
            descriptive[col]["Q2:50 %"] = dataset.describe()[col]["50%"]    
            descriptive[col]["Q3:75 %"] = dataset.describe()[col]["75%"]    
            descriptive[col]["99 %"] = np.percentile(dataset[col],99)
            descriptive[col]["Q4:100 %"] = dataset.describe()[col]["max"]
            descriptive[col]["IQR"] = dataset.describe()[col]["75%"] -  dataset.describe()[col]["25%"]
            descriptive[col]["1.5Rule"] =1.5*(dataset.describe()[col]["75%"] -  dataset.describe()[col]["25%"])
            descriptive[col]["Lesser"] =dataset.describe()[col]["25%"] - (1.5*(dataset.describe()[col]["75%"] -  dataset.describe()[col]["25%"]))
            descriptive[col]["Greater"] =dataset.describe()[col]["75%"] + (1.5*(dataset.describe()[col]["75%"] -  dataset.describe()[col]["25%"]))
            descriptive[col]["Min"] = dataset[col].min()
            descriptive[col]["Max"] = dataset[col].max()
            descriptive[col]["Skew"] = dataset[col].skew()
            descriptive[col]["Kurtosis"] = dataset[col].kurtosis()
        return descriptive

    ## Function is creating Fequency details in a table named as freqTable
    def freqTable(columnName,dataset):
        import pandas as pd
        freqTable = pd.DataFrame(columns=["Unique_values","Frequency","Relative_Frequency","Cummulative_Frequency"])
        uni_value_count=len(dataset[columnName].value_counts())
        freqTable["Unique_values"] = dataset[columnName].value_counts().index
        freqTable["Frequency"] = dataset[columnName].value_counts().values
        freqTable["Relative_Frequency"] = dataset[columnName].value_counts().values / len(dataset[columnName].value_counts())
        freqTable["Cummulative_Frequency"] = freqTable["Relative_Frequency"].cumsum()
        return freqTable

    ## Function is identifying any outlier contains in the columns and returning column names.
    def outlier_check(Quan,descriptive):
        lesser=[]
        greater=[]
        for cols in Quan:
            if descriptive[cols]["Min"]<descriptive[cols]["Lesser"]:
                lesser.append(cols)
            if descriptive[cols]["Max"]>descriptive[cols]["Greater"]:
                greater.append(cols)
        return lesser, greater

    ## Function is to replace lesser outlier value
    def replace_lesser_outlier(lesser,dataset,descriptive):
        for columnName in lesser:
            dataset[columnName][dataset[columnName]<descriptive[columnName]["Lesser"]] = descriptive[columnName]["Lesser"]
        return dataset

    ## Function is to replace greater outlier value
    def replace_greater_outlier(greater,dataset,descriptive):
        for columnName in greater:
            dataset[columnName][dataset[columnName]>descriptive[columnName]["Greater"]] = descriptive[columnName]["Greater"]
        return dataset