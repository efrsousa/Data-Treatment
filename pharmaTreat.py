import pandas as pd
import numpy as np
import math
import thread as t
#from threading import Thread
#from scipy import stats
#from IPython.display import display
#import concurrent.futures as cf
# To use this pass your file list with correct path values
# Made by Henric Pietro Vicente Gil
filess=["../../Clinical Data/Re-Filter.xlsx"]

# def multiprocessing(files:list):
    
#     for file in files:
#         with cf.ThreadPoolExecutor(max_workers=5) as exe:
#             exe.map(main,sheets)

def main(file,sheet):
    """You can also opt to pass the excel sheet list, so the program can multithread reading sheets, if you dont want to multithread sheets pass False as sheets=False and pass the sheet list in file_= sheet list"""
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

            # 30-50mg/kg
            if type(dose) is str:
                for i,n in enumerate(dose):
                    if n in ["<",">"]:
                        continue
                    if isInt(n) or n=="." and num.find(".")==-1:
                        num+=n
                    if isInt(n)==False:
                        unit+=n
                    if n in ["," ,"-", "\\", "/",""," "]:
                        nums.append(float(num))
                        num=""
                    if len(nums)>1 and "" not in nums:
                        avg=np.mean(nums)
                    elif len(nums)==0 and num!="": 
                        avg=float(num)
                # unit=[str(s) for s in number if isInt(s)==False]
                measure.append([avg, str(unit).strip(" -.")])
        
        for i,m in enumerate(measure):
            #print(m)
            u=str(m[1])
            n=m[0]
        
            if u.find("kg")!=-1 and u.find("mg")==-1:
                measure[i][0]=n*1_000_000
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
        #z_scores={}
        dct={}
        means={}
        df=df.dropna()
        
        nums=[num for num,mg in df.loc[:,value_col]]
        names=[drugs for drugs in df.loc[:,name_col]]
        
        for i,name in enumerate(names):
            
            if name not in dct:
                dct[name]=[]
                
                dct[name].append(nums[i])
                
                # z_scores[name]={"mg_values":[],"z_scores":[]}
                
            else: 
                dct[name].append(nums[i])
        
        for n in dct:
            media=[]
            if len(dct[n])>1:
                means[n]=np.mean(dct[n])
                
                if means[n]/dct[n][0]!=1:
                    std=np.std(dct[n])
                else: 
                    std=1
                
                z= z_scorer(dct[n],means[n],std)
                
                for _i,i in enumerate(z):
                    if abs(i)<=max_z:
                        media.append(dct[n][_i])
                
                med=np.mean(media)
                
                df.loc[df[name_col]==n,value_col]=med
                        # z_scores[n]["z_scores"].append(f"Z-score {i}")
                        # z_scores[n]["mg_values"].append(dct[drug][n])
                    # else: 
                    #     print(f"Outlier z-score: {i} \n Outlier mg value {n} {dct[drug][n]}")
            else:
                df.loc[df[name_col]==n,value_col]=dct[n]
            
        df=df.drop_duplicates()                
                # _=dct[n][0]
                # z_scores[n]["mg_values"]=_
                # z_scores[n]["z_scores"]=f"One entry {_}"
        #print(z_scores)
        return df

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

    def organize(file,sheet):
        """File list can also be a single file"""

        df=pd.read_excel(file,sheet_name=sheet)
        new_doses=convertTo_mg(df)
        
        df["Dose"]=new_doses
        
        z=idOutliers(df)
        z.to_excel(f"{sheet}.xlsx")
        # elif type(file_list) is list and not sheet_list:    
            #     for file in file_list:
            #         globalDf=pd.ExcelFile(file)
            #         for sheet in globalDf.sheet_names:
                        
            #             df=pd.read_excel(globalDf,sheet_name=sheet)
            #             new_doses=convertTo_mg(df)

            #             df["Dose"]=new_doses
                        
            #             z=idOutliers(df)
            #             z.to_excel(f"{sheet}.xlsx")
    organize(file,sheet)

# def multThreading(files):
#     if type(files) is str:
#         sheets=pd.ExcelFile(files).sheet_names
#         with cf.ThreadPoolExecutor(max_workers=5) as exe:
#             exe.map(main,[files,sheets])
#     else:
#         for file in files:
#             sheets=pd.ExcelFile(file).sheet_names
#             with cf.ThreadPoolExecutor(max_workers=5) as exe:
#                 exe.map(main,[file,sheets])
# multThreading(filess)