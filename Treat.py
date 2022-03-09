from IPython.display import display
import pandas as pd
#oldgetcolumn
    # def genColumnObj(table="Post-Marketing_Reports.xlsx"):
    #     df=pd.read_excel(table)
    #     obj=df.loc[:, "Adverse Events"]
    #     letterInObj=[word for word in obj]
    #     return letterInObj

def getwordsInColumn(dataframe,column):
    letterInObj=[]
    letterInObjList=[]
    for i in len(dataframe.index):
        #bj=df.iloc[i,[0,1,2,3,4,5]]
        for word in dataframe.iloc[i,column]:
            letterInObj.append(word)
        letterInObjList.append(assemble(letterInObj))
        letterInObj.clear()
    return letterInObjList

def assemble(obj):
    word=""
    words=[]
    wordsList=[]
    for letter in obj:
        word=word+letter
        word=lambda x:x.strip(",()\n")
        if letter==",":
            words.append(word.strip())
            word=""
        wordsList.append(words)
    return words

#rem
    # def rem(x):
    #     x=x.strip(" ,()")
    #     chk=""
    #     for letter in x:
    #         chk=chk+letter
    #         if chk=="\n":
    #             chk=""
    #             continue
    #     x=chk
    #     return x

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
#Adverse_eff_list=getwordsInColumn("",3)
def genWordAndNumberList(column_obj="Adverse_eff_list"):
    events=[]
    words=[]
    complete_list=[]
    contador_lista=0
    contador_palavra=0
    contador_digito=0
    for lista in Adverse_eff_list:
        contador_lista=contador_lista+1
        #print("Contador da lista %d"%contador_lista, "Contador da digito %d"%contador_digito, "Contador da palavra %d"%contador_palavra)
        for ill in lista:
            contador_palavra=contador_palavra+1
            num=""
            chk=""
            #print("Contador da palavra %d"%contador_palavra)
            for digit in ill:
                contador_digito=contador_digito+1
                if isInt(digit):
                    num=num+digit
                    
                else:
                    chk=chk+digit
                #print("Contador da digito %d"%contador_digito)
            words.append([chk.strip(" "), contador_lista-1])
            events.append([num, contador_lista-1])
        contador_palavra=0
    
    for i in range(len(words)):
        complete_list.append([words[i][0], events[i][0],events[i][1]])

    return complete_list
#effects_events=genWordAndNumberList()

#temlate dictionary
    # dictionary={
    #         "Drug": [], #[Global_df.iloc[0,0]], 
    #         "Chemical Structure": [],# Global_df.iloc[0,1], 
    #         "Reports":[],# effects_events[0][1], 
    #         "Adverse Events":[],# effects_events[0][0],
    #         "Reports by Gender":[],# Global_df.iloc[0,4],
    #         "Reports by Age":[]# Global_df.iloc[0,5]
    #         }

#Not generalized, only made for post market data
def generateNewdf(adictionary,dataframe,df_destination):
    
    local_df=pd.DataFrame([adictionary])

    m=0
    for i in len(dataframe.index):  
        print("Starting row %d"%i)  
        
        drug=dataframe.iloc[i,0]
        
        molecule=dataframe.iloc[i,1]
        
        reports_by_gender=dataframe.iloc[i,4]

        reports_by_age=dataframe.iloc[i,5]
        try:
            while effects_events[m][2]==i:
                local_df.loc[m]=[drug , molecule , effects_events[m][1] , effects_events[m][0], reports_by_gender , reports_by_age]
                m=m+1
        except IndexError:
            print(f"stopped at {m} line")
            break
    
    local_df.to_excel(df_destination)

#new_df=insertNewRows(dictionary)

#print("Input name of the new dataframe")
#new_df.to_excel(input())

