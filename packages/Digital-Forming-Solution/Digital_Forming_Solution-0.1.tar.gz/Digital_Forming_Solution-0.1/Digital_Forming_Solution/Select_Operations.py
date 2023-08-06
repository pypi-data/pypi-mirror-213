import numpy as np

def Yield_Binning(datframe,column):
    
    # Filling the Missing Values   
    datframe[column] = datframe[column].fillna(datframe[column].mean())
    
    # Calculating the yield quantiles
    col_values = list(datframe[column])
    Q_25 = np.percentile (col_values, 25) 
    Q_50 = np.percentile (col_values, 50)
    Q_75 = np.percentile (col_values, 75)

    # Creating the new column with the condtion
    for index,row in datframe.iterrows():

        if row[column] <= Q_25:
            datframe.at[index,'Category'] = 'Low'

        elif (row[column]>Q_25 and row[column] <= Q_50):
            datframe.at[index,'Category'] = 'Medium Low'

        elif (row[column]>Q_50 and row[column]<=Q_75):
            datframe.at[index,'Category'] = 'Medium High'
            
        else:
            datframe.at[index,'Category'] = 'High'
    return datframe

