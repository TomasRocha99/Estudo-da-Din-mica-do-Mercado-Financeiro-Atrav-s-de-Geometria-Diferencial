from __future__ import absolute_import, division, print_function
import numpy as np
import pandas as pd
import os
from datetime import datetime
from datetime import timedelta


def select_days(directory, beg_day, end_day):
    #Collect information from the stocks that were open on the stock exchange market on the chosen days
    #directory- location of the folder with the treated stock files
    #beg_day- the first of chosen time period
    #end_day- the first of chosen time period
    #return- dataframe with all the information on the stocks in that time period
    
    directory_list= os.listdir(directory)
    
    df1 = pd.DataFrame({'Date':[],
                        'Stock':[],
                        'Class':[],
                        'Class Name':[]})
    
    for i in directory_list:
        
        file= os.path.join(directory, i)
        path, extension_name= os.path.split(file) #Separar caminho e nome com extensão do ficheiro
        file_name, extension = os.path.splitext(extension_name) #Guardar variável com o nome da ação

        i=datetime.strptime(beg_day, '%Y-%m-%d').date()
        end =datetime.strptime(end_day, '%Y-%m-%d').date()
        
        if extension=='.txt':
            while i<= end:
            
                df = pd.read_csv(file, sep=" ", header=None, names=['Stock', 'Date', 'Class','Class Name'])
                df['Date'] = pd.to_datetime(df['Date']).dt.date

                select_day=df.loc[df['Date'] == i]           
                df1 =df1.append(select_day, ignore_index = True)
                i += timedelta(days=1)
    
    new = df1["Class"].copy()
    df1["StockClass"]= df1["Stock"].str.cat(new)
    
    new1 = df1["Class Name"].copy()
    df1["StockClassName"]= df1["Stock"].str.cat(new1)
    
    return(df1[['Date','Stock','Class','StockClass', 'StockClassName']])  

def make_dictionary(directory, beg_day, end_day):
    #Create a dictionary that the keys are all the stock-class pairs and their values are all the days that these events happened
    #directory- location of the folder with the treated stock files
    #beg_day- the first of chosen time period
    #end_day- the first of chosen time period
    #return- dictionary created
    
    df_data=select_days(directory, beg_day, end_day)

    df1=df_data['Date']
    data=df1.to_numpy() #Array with stocks names 

    
    df2=df_data['StockClassName'] 
    StockClass= df2.to_numpy() #Array with classes of the chosen stocks
    
    df_StocksClasses = pd.read_csv("Listas/AçõesClassesAcronimo.txt", sep=" ", names=['StocksClasses'])

    dictionary= {}
    
    for stockclass in df_StocksClasses['StocksClasses']:
            key = stockclass
            dictionary.update({key: [0]})

    for stockclass in dictionary.keys():
        for day in range(len(data)):
            if StockClass[day]==stockclass:
                if dictionary.get(stockclass)==[0]:
                    dictionary[stockclass].remove(0)
                dictionary[stockclass].append(data[day])

    return dictionary

def made_corpus(directory, beg_day, end_day):
    #Create and save corpus file
    #directory- location of the folder with the treated stock files
    #beg_day- the first of chosen time period
    #end_day- the first of chosen time period
    #return- none
    
    dictionary= make_dictionary(directory, beg_day, end_day)
    
    i=datetime.strptime(beg_day, '%Y-%m-%d').date()
    end =datetime.strptime(end_day, '%Y-%m-%d').date()
    
    file= os.path.join("corpus.txt") 

    f = open(file, "w") 
    while i<= end:
        for index, a in enumerate(dictionary.keys()):
            valueA = dictionary.get(a)
            for val in valueA:
                if val==i:
                    f.write(a)
                    f.write(' ')
                    continue
                    
        i += timedelta(days=1)
        f.write('.') 
        f.write('\n')
    f.close()  
    
def matriz(directory, beg_day, end_day):
    #Make the matrix for counting the number of connections for each object and the adjacency matrix for the counting of the number of links
    #directory- location of the folder with the treated stock files
    #beg_day- the first of chosen time period
    #end_day- the first of chosen time period
    #return-  matrix of connections, the number of connections of each object, the adjacency matrix, the number of links in the system
    
    dicionário=make_dictionary(directory, beg_day, end_day)
    
    matrix = np.zeros([len(dicionário.keys()), len(dicionário.keys())])
    adjc_matrix = np.zeros([len(dicionário.keys()), len(dicionário.keys())])
    
    count_connections=0
    count_links=0
    number_connections= []
    number_links= []
    
    for index, a in enumerate(dicionário.keys()):
        #print(index)
        valueA = dicionário.get(a)
        #print("valueA: ", valueA)
        
        for jndex, b in enumerate(dicionário.keys()):
            #print(jndex)
            valueB = dicionário.get(b)
            if a != b:
                #print("valueB: ", valueB)
                
                #Matrix of connections 
                for val in valueB:
                    #print(val)
                    if valueB[0] != 0 and val in valueA:
                        #print(b)
                        matrix[index, jndex] = 1
                        count_connections += 1
                        break
                #Adjacency matrix, an upper triangular matrix 
                for val in valueB:
                    if valueB[0] != 0 and val in valueA and index < jndex:
                        #print(b)
                        adjc_matrix[index, jndex] = 1
                        count_links += 1
                        break
                        
        #print("\n")
        #print(a, matrix[index,])         
        #print(a, conta_ligaçoes)
        number_connections.append(count_connections)
        number_links.append(count_links)
        count_connections=0
        count_links=0

    return matrix, number_connections, adjc_matrix, number_links

def show_matrix(directory, saveFolder, beg_day, end_day):
    #Save the number of connections for each object and show the total number of links
    #directory- location of the folder with the treated stock files
    #saveFolder- folder to retrieve data from
    #beg_day- the first of chosen time period
    #end_day- the first of chosen time period
    #return- none
    
    matrix, number_connections, adjc_matrix, number_links = matriz(directory, beg_day, end_day)
    
    df = pd.read_csv("Listas/AçõesClasses.txt", sep=" ", names=['StocksClasses'])
    df['Number of Connections']= number_connections
    #print(df)
    
    numpy_df = df.to_numpy()
    np.savetxt(os.path.join(saveFolder, "Nodes_Links.txt"), numpy_df, fmt = "%s")
    print("\n")
    print("Entaglaments counted")

    links= sum(number_links)
    print(f"The total number of links, in the geometry, is {links}")
    
    print("\n")



    
                        
           