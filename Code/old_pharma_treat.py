import numpy as np
import pandas as pd

def isObjPresent(x):
    """
    Check if obj is not a null string and exists
    """
    
    if x and x!="" :
        return True
    elif x=="" or x is None:
        return False

def areObjsPresent(*x):
    """
    Check if objs exist and are not null strings, use when multiple objs
    Returns a dictionary with the name of the inputs
    """
    ispresentList={}
    for obj in x:
        if obj and obj!="":
            ispresentList[obj]=True
        elif obj=="" or obj is None:
            ispresentList[obj]=False
    
    return ispresentList

def inputDatasetLocation():
    """
    Accepts inputs from user to dictate where the dataset can be found as well as the sheet to be analyzed, {it uses pandas to use most methods}
    If no sheet is passed the entire dataframe will be read will be considered
    Returns a dataframe  
    """
    
    print("Input dataset location to be read")
    
    file_location=input("Input File Location")
    sheet_name=input("Input sheet location, or leave it empty if theres only one sheet")
    
    try:
        areThey=areObjsPresent(file_location,sheet_name)
        
        islocation=areThey[file_location]
        
        isSheet=areThey[sheet_name]
        
        if islocation and isSheet:
            df=pd.read_excel(file_location,sheet_name=sheet_name)
        
        #debugger helper
        elif islocation==False:
            # file_location=".\\Clinical Data\\Re-Filter.xlsx"
            # df=pd.read_excel(file_location,sheet_name=sheet_name)
            print("Input file location")
            inputDatasetLocation()
        
        elif isSheet == False:
            print("Will read a random sheet")
            df=pd.read_excel(file_location,sheet_name)
        
        # dup=df.drop_duplicates()
        # num_dup=len(dup)
        # num_df=len(df)
        # print(f"{(num_df-num_dup)/100}%")
        return df
    except FileNotFoundError:
            print("Try using tabs to describe the file location")
            inputDatasetLocation()

def isInt(i):
    """Check if it is an integer"""
    try:
        int(i)
        return True
    except ValueError:
        return False

def isFloat(f):
    try:
        float(f)
        return True
    except ValueError:
        return False

def convertTo_mg(column):
    """Pass a series like (aka: df.column) of measurement strings, convert the values into miligram numbers, returns a list o lists with a number and the unit"""   
    micro="\u00B5"
    measure=[]
    past3=[]
    for number in column.tolist():
        past3.append()
        num=[n for n in number if isInt(n) or n=="."]
        unit=[str(s,"utf-8") for s in number if isInt(s)==False]
        
        measure.append([float(num),unit])
    
    for i,m in enumerate(measure):
        
        u=m[i][1]
        n=m[i][0]
        nums=[]
        if u.find("kg")!=-1:
            measure[i][0]=n*1000000
            
        #might be with special char
        elif u.find(f"{micro}g")!=-1 or unit.find("ug")!=-1:
            measure[i][0]=n/1000
        
        elif u.find("cg")!=-1:
            measure[i][0]=n*10
        
        if u.find("g")==0:
            measure[i][0]=n*1000

        nums.append(measure[i][0])
    numpy_values=np.array(nums)
    return numpy_values

def outlierRemoval(df,name_column,value_column,threshold):
    """Inform the Dataframe, inform the columns that contain the values to be analyzed, inform the treshhold to be considered when removing the outliers"""
    cols=df.loc[:,[name_column,value_column]]
    return 0

def main():
    pass