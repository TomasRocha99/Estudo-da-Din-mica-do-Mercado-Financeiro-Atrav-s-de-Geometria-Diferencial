import numpy as np
import pandas as pd
import portion as I #biblioteca para fazer intervalos
import pathlib
import os
import re


def perc_variation(file):
    #Calculatation of the percentage of daily price change for each file of a stock
    #file- cvs file from the Yahoo Finance site
    #return- dataframe with several daily information about a stock including the percentage of daily price change
    
    df = pd.read_csv(file)
    
    variation= df['Adj Close']-df['Open'] #Calculatation of the daily price change 
    df['Variation'] = variation
    
    percentage_variation= df['Variation']/df['Open'] *100 #Calculatation of the percentage of daily price change
    df['Perc Variation'] = percentage_variation 
    
    return df
    
    
def perc_class(file):
    #Allocation of each percentage of daily price change to the designated class and identification of the same class
    #file- cvs file from the Yahoo Finance site
    #return- dataframe of the function above, with each percentage class and each class name
    
    df = perc_variation(file)
    limits_class=[I.openclosed(-I.inf, -2), I.openclosed(-2, -1.5), I.openclosed(-1.5, -1), I.openclosed(-1, -0.5), I.openclosed(-0.5, 0), I.openclosed(0, 0.5), I.openclosed(0.5, 1),I.openclosed(1, 1.5), I.openclosed(1.5, 2), I.open(2, I.inf)] #Criação dos intervalos de classes
    acronyms =[["AAA"], ["BBB"], ["CCC"], ["DDD"], ["EEE"], ["FFF"], ["GGG"], ["HHH"], ["III"], ["JJJ"]]

    classes= []
    
    for i in  df['Perc Variation']: #Definition of a class for each percentage of daily price change
        for j in limits_class:
            if i in j:
                classes+=j
    
    df['Class'] = classes 
    
    class_name= []
    for i in  df['Class']: #identification of each class with its acronym
        for j in range(len(limits_class)):
            if i == limits_class[j]:
                class_name+=acronyms[j]
    
   
    df['Class Name'] = class_name 
    
    return df


def save(directory): 
    #Save the treated files into a folder
    #directory- location of the folder with the cvs files from the Yahoo Finance site
    #return- none
    
    directory_list= os.listdir(directory)
    
    for i in directory_list:
        
        file_not_treated= os.path.join(directory, i)
        
        path, extension_name= os.path.split(file_not_treated) #Break apart the path and the extension name of the file location
        file_name, extension = os.path.splitext(extension_name) #Save the stock name

        clean_file_name = re.sub("[^a-zA-Z]","", file_name)

        if extension=='.csv':
            df= perc_class(file_not_treated)
            df['Stock'] = clean_file_name
            
            df1 = df[['Stock','Date','Class','Class Name']]
                          
            if not os.path.exists(path+'/Treated'):
                os.makedirs(path+'/Treated')
    
            file= os.path.join(path+'/Treated', clean_file_name+ ".txt") 

            f = open(file, "w") 
        
            np.savetxt(file, df1.values, fmt='%s')
        
            f.close()
    
#------------------------------------------- Control Communication ----------------------------------------------------        
def validateFunction(choice, type):   
    
    
    # Check if choice is empty
    if (not choice):
        return False, -1
    
    
    directory_list=os.listdir(pathlib.Path().absolute())
    
    # Verifies input for the option of the folder
    if (type == "folder"):
        
        validationCondition= False
        for i in directory_list:
            if choice == i:
                validationCondition = True

        return validationCondition, choice

   
# Loop controling variables
run = True
menu = True

# Menu Loop
while (run):  
    
    # User menu
    if (menu):
        print("Do you want to treat stocks files?") 
        
        folder = input(f"Input the name of the folder containing the files you want to clean: ")
        
        # Validate answer - folder
        validationCondition, folder = validateFunction(folder, "folder")

        while (not validationCondition):
            folder = input(f"Input is not valid. Must be an existing folder in the same directory of this Python script. Try again: ")
            validationCondition, folder = validateFunction(folder, "folder") 
        
        save(folder)
        
        print()
        print("All files have been treated")
        menu = False
        close= True
        
    # End program menu
    while (close):
        print()
        endOption = input("End program (y/n)? ")

        if (endOption == "y" or endOption == "Y"):
            run = False
            close = False

        elif (endOption == "n" or endOption == "N"):
            menu = True
            close = False
            print()
        else:
            print("Input not valid. Please try again: ")
    
    
    
    

