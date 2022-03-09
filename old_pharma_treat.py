import pandas as pd
import numpy as np
import math
from IPython.display import display
import concurrent.futures as cf
# Toxic Hepatitis
# .\Clinical Data\Filtered_Clinical_Data.xlsx
# Filtered Toxic Hepatitis

file=[".\Clinical Data\Filtered_Clinical_Data.xlsx",".\Pre Clinical Data\Dose_Filtered_Hepato_Data.xlsx"]
#sheet=input("Input Sheet name: ")

def readExcel(file,sheet):
    df=pd.read_excel(file,sheet_name=sheet)
    return df

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

def convertTo_mg(df,column="Dose"):
    """Pass a series like (aka: df.column) of measurement strings, convert the values into miligram numbers, returns a list o lists with a number and the unit"""   
    
    micro="\u00B5"
    measure=[]
    
    for dose in df.loc[:,column]:
        # num=[n for n in number if isInt(n) or n=="."]
        num=""
        unit=""
        nums=[]
        if type(dose) is str:
            for i,n in enumerate(dose):
                if isInt(n) or n=="." and num.find(".")==-1:
                    num+=n
                if isInt(n)==False:
                    unit+=n
                if n in ["," ,"-", "\\", "/",""," "]:
                    nums.append(num)
                    num=""
                if len(nums)>1 and "" not in nums:
                    avg=(float(nums[0])+float(nums[1]))/2
                
                elif len(nums)==0 and num!="": avg=float(num)
            # unit=[str(s) for s in number if isInt(s)==False]
            measure.append([avg,str(unit).strip(" -<>.")])
    
    for i,m in enumerate(measure):
        #print(m)
        u=str(m[1])
        n=m[0]
    
        if u.find("kg")!=-1 and u.find("mg")==-1:
            measure[i][0]=n*1000000
            measure[i][1]=str(measure[i][1]).replace("kg","mg")
            
        #might be with special char
        elif u.find(f"{micro}g")!=-1 or unit.find("ug")!=-1:
            measure[i][0]=n/1000
            measure[i][1]=str(measure[i][1]).replace("ug","mg")
        elif u.find("cg")!=-1:
            measure[i][0]=n*10
            measure[i][1]=str(measure[i][1]).replace("cg","mg")
        if u.find("g")==0:
            measure[i][0]=n*1000
            measure[i][1]=str(measure[i][1]).replace("g","mg")
    
    solved_col=pd.Series(measure)
        
    return solved_col

def stdCalculation(numList,mean):
    n=len(numList)+1
    soma=0
    for x in numList:
        soma+=(x-mean)**2
    std=math.sqrt((soma)/n)
    return std
        
def z_scorer(nums: list,mean: float or int,std: float or int):
    z_scores=[]
    for x in nums:
        z=(x-mean)/std
        z_scores.append(z)
    return z_scores

def idOutliers(df: pd.DataFrame,name_col: str="Drug",value_col: str="Dose",max_z: float=1.8):
    z_scores={}
    dct={}
    means={}
    df=df.dropna()
    
    nums=[num for num,mg in df.loc[:,value_col]]
    names=[drugs for drugs in df.loc[:,name_col]]
    
    for i,name in enumerate(names):
        if name not in dct:
            dct[name]=[]
            dct[name].append(nums[i])
            z_scores[name]={
                "mg_values":[],
                "z_scores":[]
                }
            
        else: 
            dct[name].append(nums[i])
    
    for drug in dct:
        
        if len(dct[drug])>1:
            means[drug]=np.mean(dct[drug])
            
            if means[drug]/dct[drug][0]!=1:
                std=stdCalculation(dct[drug],means[drug])
            else: 
                std=1
            
            z= z_scorer(dct[drug],means[drug],std)
            
            for n,i in enumerate(z):
                if abs(i)<=max_z:
                    z_scores[drug]["z_scores"].append(f"Z-score {i}")
                    z_scores[drug]["mg_values"].append(dct[drug][n])
                # else: 
                #     print(f"Outlier z-score: {i} \n Outlier mg value {drug} {dct[drug][n]}")
        else: 
            _=dct[drug][0]
            z_scores[drug]["mg_values"]=_
            z_scores[drug]["z_scores"]=f"One entry {_}"
    #print(z_scores)
    return z_scores
            


def treat_df(z_scored):
        dct={}
        for drug in z_scored:
            for key,value in z_scored[drug].items():
                if key=="mg_values":
                    if type(value)is float:
                        dct[drug]=value
                        
                    else:
                        dct[drug]=np.mean(value)
        series_obj=pd.DataFrame({"Drug":dct.keys(),"Dose":dct.values()})
        return series_obj

def main(file_list:list):
    for file in file_list:
        globalDf=pd.ExcelFile(file)
        for sheet in globalDf.sheet_names:
            #Dose=globalDf["Dose"]
            df=pd.read_excel(globalDf,sheet_name=sheet)
            new_doses=convertTo_mg(df)
            df["Dose"]=new_doses
            #display(df)
            
            z_scored=idOutliers(df)
            z=treat_df(z_scored)
            df=df.drop_duplicates()
            print(z)
main(file)