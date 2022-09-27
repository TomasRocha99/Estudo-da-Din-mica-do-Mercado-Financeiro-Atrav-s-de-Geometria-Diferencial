import pandas as pd
import portion as I #biblioteca para fazer intervalos
import os
import re

def escolher_dia(directoria, dia):
    lista_directoria= os.listdir(directoria)
    
    df1 = pd.DataFrame({'Data':[],
                        'Ação':[],
                        'Classe':[]})
    
    for i in lista_directoria:
        
        file= os.path.join(directoria, i)
        caminho, nome_extensao= os.path.split(file) #Separar caminho e nome com extensão do ficheiro
        nome_ficheiro, extensao = os.path.splitext(nome_extensao) #Guardar variável com o nome da ação
        
        
        if extensao=='.txt':
            df = pd.read_csv(file, sep=" ", header=None, names=['Ação', 'Data', 'Classe', 'Nome Classe'])
            select_dia=df.loc[df['Data'] == dia]           
            df1 =df1.append(select_dia, ignore_index = True)
    print(df1)
    return(df1[['Ação','Data','Classe']])  

def lista_Ações(directoria,dia):
    df= escolher_dia(directoria, dia)
    ação_N=df['Ação'].to_numpy()

    with open("Listas/Nome_Ações.txt", 'w') as f:
        for ação in ação_N:
            ação_limpa = re.sub("[^a-zA-Z]","", ação)
            f.write(str(ação) + '\n')
            
def lista_Classes():
    
    classes=[I.openclosed(-I.inf, -2), I.openclosed(-2, -1.5), I.openclosed(-1.5, -1), I.openclosed(-1, -0.5), I.openclosed(-0.5, 0), I.openclosed(0, 0.5), I.openclosed(0.5, 1),I.openclosed(1, 1.5), I.openclosed(1.5, 2), I.open(2, I.inf)] #Criação dos intervalos de classes    
    
    with open("Listas/Classes.txt", 'w') as f:
        for classe in classes:
            f.write(str(classe) + '\n')
            
def lista_AçãoClasses():
    df = pd.read_csv("Listas/Nome_Ações.txt", sep=" ", names=['Ação'])
    
    classes=[I.openclosed(-I.inf, -2), I.openclosed(-2, -1.5), I.openclosed(-1.5, -1), I.openclosed(-1, -0.5), I.openclosed(-0.5, 0), I.openclosed(0, 0.5), I.openclosed(0.5, 1),I.openclosed(1, 1.5), I.openclosed(1.5, 2), I.open(2, I.inf)] #Criação dos intervalos de classes    
    
    with open("Listas/AçõesClasses.txt", 'w') as f:
        for ind in df.index:
            for classe in classes:
                f.write(df['Ação'][ind]+ str(classe) + '\n')
                
def lista_AçãoClassesAcronimo():
    df = pd.read_csv("Listas/Nome_Ações.txt", sep=" ", names=['Ação'])
    
    acronimos_classes=["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH", "III", "JJJ"]
    
    with open("Listas/AçõesClassesAcronimo.txt", 'w') as f:
        for ind in df.index:
            for acronimos in acronimos_classes:
                f.write(df['Ação'][ind]+ str(acronimos) + '\n')
                
                
                
                
                
                