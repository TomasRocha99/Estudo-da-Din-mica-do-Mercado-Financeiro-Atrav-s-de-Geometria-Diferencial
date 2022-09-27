# Script used to create the model. Adapted from the code written by Laura Elvas in his master degree thesis "Estudos de Variação de Densidade num Espaço Inflacionário".

# Menu script to facilitate the creation of data

# Possible Actions:
# - Create models, 2D and 3D dataframes in a given interval, saving them and plot them
# - Load all the created dataframes and plot them

import os
from datetime import datetime
import gensim.models.word2vec as w2v

import DataCreator


# Always print to console
import functools
print = functools.partial(print, flush=True)

#--------------------------------------- CONFIGURATIONS ----------------------------------------------

# Change these variables if there is an increase in data and more years are added and if the maximum number of years before a checkpoint is reached needs to be bigger
minDay  = '2021-04-05'
maxDay  = '2022-04-04'

#Change if the directory of treated files change
directory='Ações 1 ano 4.04/Treated'
#------------------------------------------- CODE ----------------------------------------------------

# Changes in the following code may break it

def validateFunction(choice, type):
    # Verifies if the value is in accordance with the type of action made
    # choice   - value of the choice made
    # type     - type of validation to be made, "option", "interval", "checkpoint", "dimension" or "metric"
    # return   - wether value is valid or not and choice, -1 is invalidity of the choice or type

    # Check if choice is empty
    if (not choice):
        return False, -1

    # Verifies input for the option menu
    if (type == "option"):
        validationCondition = (choice == "1") or (choice == "2") or (choice == "3")

        return validationCondition, -1
    
    # Verifies input for the first day
    if (type == "day"):
        
        try:
            validationCondition = bool(datetime.strptime(choice, '%Y-%m-%d'))
        except ValueError:
            validationCondition=False
            return False, -1
        
        if (not validationCondition):
            return False, -1 
        else:
            min_Day = datetime.strptime(minDay, '%Y-%m-%d')
            max_Day = datetime.strptime(maxDay, '%Y-%m-%d')
            day = datetime.strptime(choice, '%Y-%m-%d')
            
            validationCondition= (day <= max_Day) and (day >= min_Day)
            
            if(not validationCondition):
                return False, -1
            
        return True, choice
    
    # Verifies input for the dimension
    if (type == "dimension"):
        validationCondition = (choice == "2") or (choice == "3") or (choice == "both")
    
        if (choice.isnumeric()):
            choice = int(choice)
    
        return validationCondition, choice
    
    # Verifies input for the metric
    if (type == "metric"):
        validationCondition = (choice == "cosine") or (choice == "dot") or (choice == "both")
    
        return validationCondition, choice

    # Verifies input for the second option menu
    if (type == "option2"):
        validationCondition = (choice == "1") or (choice == "2") or (choice == "3")

        return validationCondition, -1
    
    # Verifies input for the top similar words
    if (type == "top"):
        validationCondition= False

        if choice.isnumeric():
            validationCondition = True

        return validationCondition, -1
    
    return False, -1


# Loop controling variables
run = True
menu = True

# Menu Loop
while (run):

    # User menu
    if (menu):
        print("What would you like to do?")
        print("1 - Create models and 2D or 3D dataframes in a given interval, saving them and plot them")
        print("2 - Load and visualise previously created data")
        print("3 - Load and study of the similarity of words")

        print()
        print("Warning:")
        print("- Creation actions will not show the plots but will save them in the correct folders")
        print("- Never add empty space before or after commas or \"-\"")

        option = input()

        # Validate answer - option
        validationCondition1, _ = validateFunction(option, "option")
        while (not validationCondition1):
            option = input("Input is neither 1, 2 or 3. Try again: ")
            validationCondition1, _ = validateFunction(option, "option")

        print()
        
        dimension = input(f"Input if data created must be 2D, 3D or both (2 for 2D, 3 for 3D or word \"both\"): ")
        
        # Validate answer - dimension
        validationCondition2, dimension = validateFunction(dimension, "dimension")

        while (not validationCondition2):
            dimension = input(f"Input is not valid. Must be 2, 3 or word \"both\". Try again: ")
            validationCondition2, dimension = validateFunction(dimension, "dimension")

        metric = input(f"Input if data created is based on cosine similarity, dot product or both (cosine for cosine similarity, dot for dot product or word \"both\"): ")

        # Validate answer - metric
        validationCondition3, metric = validateFunction(metric, "metric")

        while (not validationCondition3):
            metric = input(f"Input is not valid. Must be cosine, dot or word \"both\". Try again: ")
            validationCondition3, metric = validateFunction(metric, "metric")

        menu = False
	
    # Option 1 - Create models and 2D or 3D dataframes in a given interval, saving them and plot them
    if (option == "1"):
        
        print()
        begDay = input(f"Input the first day of the data from {minDay} to {maxDay} in the form YYYY-MM-DD (ex. {minDay}): ")
        
	    # Validate answer - begDay
        validationCondition4, begDay = validateFunction(begDay, "day")

        while (not validationCondition4):
            begDay = input(f"Input is not valid. Must be of the form #YYYY-MM-DD with no space before or after commas or \"-\" and between {minDay} to {maxDay}. Try again: ")
            validationCondition4, begDay = validateFunction(begDay, "day")

        print()
        endDay = input(f"Input the last day of the data from {minDay} to {maxDay} in the form YYYY-MM-DD (ex. {maxDay}): ")
        
	    # Validate answer - endDay
        validationCondition4, endDay = validateFunction(endDay, "day")

        while (not validationCondition4):
            endDay = input(f"Input is not valid. Must be of the form #YYYY-MM-DD with no space before or after commas or \"-\" and between {minDay} to {maxDay}. Try again: ")
            validationCondition4, endDay = validateFunction(endDay, "day")
        
        begData = datetime.strptime(begDay, '%Y-%m-%d')
        endData = datetime.strptime(endDay, '%Y-%m-%d')
        
        # Verifie if the first day is before the last
        validationCondition5=True
        if (begData >= endData):
            validationCondition5= False
        
        while (not validationCondition5):
            endDay = input(f"Input is not valid. Must be a day after the first day {begDay}. Try again: ")
            validationCondition5= True
            validationCondition4, endDay = validateFunction(endDay, "day")
            while (not validationCondition4):
                endDay = input(f"Input is not valid. Must be of the form #YYYY-MM-DD with no space before or after commas or \"-\" and between {minDay} to {maxDay}. Try again: ")
                validationCondition4, endDay = validateFunction(endDay, "day")
            endData = datetime.strptime(endDay, '%Y-%m-%d')
            if (begData >= endData):
                validationCondition5= False      
              
        # Create save folder
        saveFolder = os.path.join("Saved Data", str(begDay) + "_" + str(endDay))
    
        if not os.path.exists(saveFolder):
            os.makedirs(saveFolder)
        
        # Create data           
        DataCreator.dataCreator(directory, begDay, endDay, saveFolder)
        
        if (dimension == "both"):
            # Load data
            dataListComplete2D, dataListComplete3D, limitsDict2D, limitsDict3D = DataCreator.loadData(begDay, endDay, metric, dimension, saveFolder)
        
            # Plot data
            DataCreator.plotGlobal2D(begDay, endDay, dataListComplete2D, limitsDict2D, False, True, saveFolder)
            DataCreator.plotGlobal3D(begDay, endDay, dataListComplete3D, limitsDict3D, False, True, saveFolder)
        else:
            # Load data
            dataListComplete, limitsDict = DataCreator.loadData(begDay, endDay, metric, dimension, saveFolder)
    
            # Plot data
            if (dimension == 2):
                DataCreator.plotGlobal2D(begDay, endDay, dataListComplete, limitsDict, False, True, saveFolder)
            elif (dimension == 3):
                DataCreator.plotGlobal3D(begDay, endDay, dataListComplete, limitsDict, False, True, saveFolder)
        close = True
        
    # Option 2 - Load and visualise previously created data
    if (option == "2"):
        # Check if data exists
        validationCondition6 = False
        while (not validationCondition6):
            print()
            begDay = input(f"Input the first day of the data from {minDay} to {maxDay} in the form YYYY-MM-DD (ex. {minDay}): ")
            
            #Validate answer - begDay
            validationCondition4, begDay = validateFunction(begDay, "day")
            
            while (not validationCondition4):
                begDay = input(f"Input is not valid. Must be of the form #YYYY-MM-DD with no space before or after commas or \"-\" and between {minDay} to {maxDay}. Try again: ")
                validationCondition4, begDay = validateFunction(begDay, "day")
            
            print()
            
            endDay = input(f"Input the last day of the data from {minDay} to {maxDay} in the form YYYY-MM-DD (ex. {maxDay}): ")
            
            #Validate answer - endDay
            validationCondition4, endDay = validateFunction(endDay, "day")
            
            while (not validationCondition4):
                endDay = input(f"Input is not valid. Must be of the form #YYYY-MM-DD with no space before or after commas or \"-\" and between {minDay} to {maxDay}. Try again: ")
                validationCondition4, endDay = validateFunction(endDay, "day")
            
            begData = datetime.strptime(begDay, '%Y-%m-%d')
            endData = datetime.strptime(endDay, '%Y-%m-%d')
            
            # Verifie if the first day is before the last
            validationCondition5=True
            if (begData >= endData):
                validationCondition5= False
            
            while (not validationCondition5):
                endDay = input(f"Input is not valid. Must be a day after the first day {begDay}. Try again: ")
                validationCondition5= True
                validationCondition4, endDay = validateFunction(endDay, "day")
                while (not validationCondition4):
                    endDay = input(f"Input is not valid. Must be of the form #YYYY-MM-DD with no space before or after commas or \"-\" and between {minDay} to {maxDay}. Try again: ")
                    validationCondition4, endDay = validateFunction(endDay, "day")
                endData = datetime.strptime(endDay, '%Y-%m-%d')
                if (begData >= endData):
                    validationCondition5= False
                    
            # Create save folder
            saveFolder = os.path.join("Saved Data", str(begDay) + "_" + str(endDay))
    
            if (not os.path.exists(saveFolder)):
                print()
                print("No data created with the information chosen. Try again")
            else:
                validationCondition6 = True
        
        if (dimension == "both"):
            # Load data
            dataListComplete2D, dataListComplete3D, limitsDict2D, limitsDict3D = DataCreator.loadData(begDay, endDay, metric, dimension, saveFolder)
        
            # Plot data
            DataCreator.plotGlobal2D(begDay, endDay, dataListComplete2D, limitsDict2D, False, True, 1)
            DataCreator.plotGlobal3D(begDay, endDay, dataListComplete3D, limitsDict3D, False, True, saveFolder)
        else:
            # Load data
            dataListComplete, limitsDict = DataCreator.loadData(begDay, endDay, metric, dimension, saveFolder)

            # Plot data
            if (dimension == 2):
                DataCreator.plotGlobal2D(begDay, endDay, dataListComplete, limitsDict, False, True, saveFolder)
            elif (dimension == 3):
                DataCreator.plotGlobal3D(begDay, endDay, dataListComplete, limitsDict, False, True, saveFolder)
                
    # Option 3 - Load and study of the similarity of words
    if (option == "3"):
        # Check if data exists
        validationCondition6 = False
        while (not validationCondition6):
            print()
            begDay = input(f"Input the first day of the data from {minDay} to {maxDay} in the form YYYY-MM-DD (ex. {minDay}): ")
            
            #Validate answer - begDay
            validationCondition4, begDay = validateFunction(begDay, "day")
            
            while (not validationCondition4):
                begDay = input(f"Input is not valid. Must be of the form #YYYY-MM-DD with no space before or after commas or \"-\" and between {minDay} to {maxDay}. Try again: ")
                validationCondition4, begDay = validateFunction(begDay, "day")
            
            print()
            
            endDay = input(f"Input the last day of the data from {minDay} to {maxDay} in the form YYYY-MM-DD (ex. {maxDay}): ")
            
            #Validate answer - endDay
            validationCondition4, endDay = validateFunction(endDay, "day")
            
            while (not validationCondition4):
                endDay = input(f"Input is not valid. Must be of the form #YYYY-MM-DD with no space before or after commas or \"-\" and between {minDay} to {maxDay}. Try again: ")
                validationCondition4, endDay = validateFunction(endDay, "day")
            
            begData = datetime.strptime(begDay, '%Y-%m-%d')
            endData = datetime.strptime(endDay, '%Y-%m-%d')
            
            # Verifie if the first day is before the last
            validationCondition5=True
            if (begData >= endData):
                validationCondition5= False
            
            while (not validationCondition5):
                endDay = input(f"Input is not valid. Must be a day after the first day {begDay}. Try again: ")
                validationCondition5= True
                validationCondition4, endDay = validateFunction(endDay, "day")
                while (not validationCondition4):
                    endDay = input(f"Input is not valid. Must be of the form #YYYY-MM-DD with no space before or after commas or \"-\" and between {minDay} to {maxDay}. Try again: ")
                    validationCondition4, endDay = validateFunction(endDay, "day")
                endData = datetime.strptime(endDay, '%Y-%m-%d')
                if (begData >= endData):
                    validationCondition5= False
                    
            # Create save folder
            saveFolder = os.path.join("Saved Data", str(begDay) + "_" + str(endDay))
    
            if (not os.path.exists(saveFolder)):
                print()
                print("No data created with the information chosen. Try again")
            else:
                validationCondition6 = True
    
            # Name of the model
            modelName = "Model_" + str(begDay) + "_" + str(endDay)
            
            # Check if trained model already exists
            if (os.path.exists(os.path.join(saveFolder, modelName + ".w2v"))):
                model = w2v.Word2Vec.load(os.path.join(saveFolder, modelName + ".w2v"))  
            
            print()
            print("What would you like to do?")
            print("1 - Study the words most similar to a specific one")
            print("2 - Study the similarity between two words")

            option2 = input()

            # Validate answer - option2
            validationCondition7, choice = validateFunction(option2, "option2")
            while (not validationCondition7):
                option2 = input("Input is neither 1 or 2. Try again:")
                validationCondition7, choice = validateFunction(option2, "option2")
    

            # Option2 1 - Study the words most similar to a specific one
            if (option2 == "1"):
                
                print()
                word = input("Input the word to see its most similar words:")
                
                #Validate the word
                if word not in model.wv.key_to_index:
                    validationCondition8= False
                else:
                    validationCondition8= True
                    
                while (not validationCondition8):
                    word = input("Input is not valid. Must be a word that is in the model vocabulary. Try again:")
                    if word not in model.wv.key_to_index:
                        validationCondition8= False
                    else:
                        validationCondition8= True
                
                print()
                top = input("Input how many similar words you want to see. This must be a number:")
                
                # Validate answer - top
                top= top.replace(" ", "")
                validationCondition9, choice = validateFunction(top, "top")
                
                while (not validationCondition9):
                    top = input("Input is not valid. Value must be numeric. Try again:")
                    top= top.replace(" ", "")
                    validationCondition9, choice = validateFunction(top, "top")
                
                DataCreator.top_similiar_words(model, word, top)
            
            # Option2 2 - Study the similarity between two words
            if (option2 == "2"):
                
                print()
                word1 = input("Input the first word to see its similarity:")
                
                #Validate the word1
                if word1 not in model.wv.key_to_index:
                    validationCondition10= False
                else:
                    validationCondition10= True
                    
                while (not validationCondition10):
                    word1 = input("Input is not valid. Must be a word that is in the model vocabulary. Try again:")
                    if word1 not in model.wv.key_to_index:
                        validationCondition10= False
                    else:
                        validationCondition10= True
                        
                print()
                word2 = input("Input the second word to see its similarity with the first one:")
                
                #Validate the word1
                if word2 not in model.wv.key_to_index:
                    validationCondition11= False
                else:
                    validationCondition11= True
                    
                while (not validationCondition11):
                    word2 = input("Input is not valid. Must be a word that is in the model vocabulary. Try again:")
                    if word2 not in model.wv.key_to_index:
                        validationCondition11= False
                    else:
                        validationCondition11= True
                
                DataCreator.similarity_2_words(model, word1, word2)
            
        print()
        close = True
        
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
