# Script used to create the model. Adapted from the code written by Laura Elvas in his master degree thesis "Estudos de Variação de Densidade num Espaço Inflacionário".

# Functions in this script are responsible for:
# - Creating models in a given interval and saving them at given checkpoints
# - Creating 2D and 3D dataframes from the models with the entire vocabulary
# - Loading all the dataframes and plotting them

import os
import matplotlib.pyplot as plt
import pandas as pd
import gensim.models.word2vec as w2v

import ProcessCorpus
import ModelTraining
import DimensionReduction
import WordSpacePlot

# Always print to console
import functools
print = functools.partial(print, flush=True)

# Create save general folder
if not os.path.exists("Saved Data"):
    os.makedirs("Saved Data")
    
def dataCreator(directory, beg, end, saveFolder):
    # Creates and trains a model for a given year interval, saving the model state in a dataframe at user-defined checkpoints. The calculations are based on the cosine similarity and dot product
    # directory  - location of the folder with the treated stock files
    # beg        - first day of the interval
    # end        - last day of the interval
    # saveFolder - folder to save data
    # return     - none
    
    #Create the corpus for the study
    process_corpus = ProcessCorpus.made_corpus(directory, beg, end)
    
    #Count the number of entanglements for each element of the vocabulary
    process_count= ProcessCorpus.show_matrix(directory, saveFolder, beg, end)
    
    # Name of the model
    modelName = "Model_" + str(beg) + "_" + str(end)
    
    # Check if trained model already exists
    if (os.path.exists(os.path.join(saveFolder, modelName + ".w2v"))):
        model = w2v.Word2Vec.load(os.path.join(saveFolder, modelName + ".w2v"))

        model = ModelTraining.createModel('corpus.txt', saveFolder, modelName, model)

    else:
        # If no model exists, create one
        model = ModelTraining.createModel('corpus.txt', saveFolder, modelName)
        print('DataCreator model:')
        print(model)


    print()
    print(f"Model for {beg} till {end} created")
    print()

    if (not os.path.exists(os.path.join(saveFolder, "dataframeComplete3D_.csv"))):
        # Reduce the dimension and produce a 3D dataframe - calculations cosine similarity
        matrix = DimensionReduction.reduceDimension(model, saveFolder, 3, "cosine")
        dataframe3D = WordSpacePlot.createDataframe(model, matrix, 3)
        dataframe3D.to_csv(os.path.join(saveFolder, "dataframeComplete3D_.csv"), index = False)
        print("Global 3D dataframes created - cosine similarity")

    if (not os.path.exists(os.path.join(saveFolder, "dataframeComplete2D_.csv"))):
        # Reduce the dimension and produce a 2D dataframe - calculations cosine similarity
        matrix = DimensionReduction.reduceDimension(model, saveFolder, 2, "cosine")
        dataframe2D = WordSpacePlot.createDataframe(model, matrix, 2)
        dataframe2D.to_csv(os.path.join(saveFolder, "dataframeComplete2D_.csv"), index = False)
        print("Global 2D dataframes created - cosine similarity")
        
           
    if (not os.path.exists(os.path.join(saveFolder, "dataframeComplete3D_dot_.csv"))):
        # Reduce the dimension and produce a 3D dataframe - calculations dot product
        matrix = DimensionReduction.reduceDimension(model, saveFolder, 3, "dotProduct")
        dataframe3D_dot = WordSpacePlot.createDataframe(model, matrix, 3)
        dataframe3D_dot.to_csv(os.path.join(saveFolder, "dataframeComplete3D_dot_.csv"), index = False)
        print("Global 3D dataframes created - dot product")

    if (not os.path.exists(os.path.join(saveFolder, "dataframeComplete2D_dot_.csv"))):
        # Reduce the dimension and produce a 2D dataframe - calculations dot product
        matrix = DimensionReduction.reduceDimension(model, saveFolder, 2, "dotProduct")
        dataframe2D_dot = WordSpacePlot.createDataframe(model, matrix, 2)
        dataframe2D_dot.to_csv(os.path.join(saveFolder, "dataframeComplete2D_dot_.csv"), index = False)
        print("Global 2D dataframes created - dot product")

    return None

def loadData(beg, end, metric, dimension, saveFolder):
    # Loads the dataframes previously created by dataCreator based on the metric chosen and dimension
    # beg        - first day of the interval
    # end        - last day of the interval
    # metric     - metric to consider when loading dataframes ("cosine" - loads dataframes created based on the cosine similarity, "dot" - loads dataframes created based on the dot product, "both" - loads all dataframes)
    # dimension  - dimension to load (2 - loads 2D dataframes, 3 - loads 3D dataframes, "both" - loads all dataframes)
    # saveFolder - folder to retrieve data from
    # return     - lists with all the years to parse, chosen dataframes and their global limits dictionary
    
    # Important lists
    if (dimension == 2 or dimension == "both"):
        dataListComplete2D = [] # List saving 2D dataframes of all words for each plot
        if (metric == "dot" or  metric == "both"):
            dataListCompleteDot2D = [] # Temporary list saving 2D dataframes of all words for each plot created based on the dot product
    
    if (dimension == 3 or dimension == "both"):
        dataListComplete3D = [] # List saving 3D dataframes of all words for each plot
        if (metric == "dot" or  metric == "both"):
            dataListCompleteDot3D = [] # Temporary list saving 3D dataframes of all words for each plot created based on the dot product

    # Dictionary initialization
    keys2D = ["limMinX", "limMaxX", "limMinY", "limMaxY", "limMinXDot", "limMaxXDot", "limMinYDot", "limMaxYDot"]
    keys3D = ["limMinX", "limMaxX", "limMinY", "limMaxY", "limMinZ", "limMaxZ", "limMinXDot", "limMaxXDot", "limMinYDot", "limMaxYDot", "limMinZDot", "limMaxZDot"]

    limitsDict2D = {key: 0 for key in keys2D} # Dictionary with the global 2D limits for all plots
    limitsDict3D = {key: 0 for key in keys3D} # Dictionary with the global 3D limits for all plots

    dataFolders=[]
    for folder in os.listdir(saveFolder):
        file_name, extension = os.path.splitext(folder) 
        if extension=='.csv':
            dataFolders.append(folder)
    
    print()
    print("Loading data...")


    for file in dataFolders:
        fileSplit = file.split("_")

        if (dimension == 3 or dimension == "both"):
            # Load dataframeComplete3D
            if(fileSplit[0] == "dataframeComplete3D" and not fileSplit[1] == "dot" and (metric == "cosine" or metric == "both")):
                dataComplete = pd.read_csv(os.path.join(saveFolder,file))
                dataListComplete3D.append(dataComplete)

                # Calculate the global 3D limits, the limits are shared by all global plots
                #if (limitsDict3D["limMinX"] > min(dataComplete.x)):
                limitsDict3D["limMinX"] = min(dataComplete.x)

                limitsDict3D["limMaxX"] = max(dataComplete.x)

                limitsDict3D["limMinY"] = min(dataComplete.y)

                limitsDict3D["limMaxY"] = max(dataComplete.y)

                limitsDict3D["limMinZ"] = min(dataComplete.z)

                limitsDict3D["limMaxZ"] = max(dataComplete.z)

                print("Global 3D dataframes loaded - cosine similarity")

            # Load dataframeComplete3D_dot
            if(fileSplit[0] == "dataframeComplete3D" and fileSplit[1] == "dot" and (metric == "dot" or metric == "both")):
                dataComplete = pd.read_csv(os.path.join(saveFolder, file))
                dataListCompleteDot3D.append(dataComplete)

                # Calculate the global 3D limits, the limits are shared by all global plots
                #if (limitsDict3D["limMinXDot"] > min(dataComplete.x)):
                limitsDict3D["limMinXDot"] = min(dataComplete.x)

                limitsDict3D["limMaxXDot"] = max(dataComplete.x)

                limitsDict3D["limMinYDot"] = min(dataComplete.y)

                limitsDict3D["limMaxYDot"] = max(dataComplete.y)

                limitsDict3D["limMinZDot"] = min(dataComplete.z)

                limitsDict3D["limMaxZDot"] = max(dataComplete.z)

                print("Global 3D dataframes loaded - dot product")

        if (dimension == 2 or dimension == "both"):

            # Load dataframeComplete2D
            if(fileSplit[0] == "dataframeComplete2D" and not fileSplit[1] == "dot" and (metric == "cosine" or metric == "both")):
                dataComplete = pd.read_csv(os.path.join(saveFolder, file))
                dataListComplete2D.append(dataComplete)

                # Calculate the global 2D limits, the limits are shared by all global plots
                limitsDict2D["limMinX"] = min(dataComplete.x)

                limitsDict2D["limMaxX"] = max(dataComplete.x)

                limitsDict2D["limMinY"] = min(dataComplete.y)

                limitsDict2D["limMaxY"] = max(dataComplete.y)

                print("Global 2D dataframes loaded - cosine similarity")

                        
            # Load dataframeComplete2D_dot
            if(fileSplit[0] == "dataframeComplete2D" and fileSplit[1] == "dot" and (metric == "dot" or metric == "both")):
                dataComplete = pd.read_csv(os.path.join(saveFolder, file))
                dataListCompleteDot2D.append(dataComplete)

                # Calculate the global 2D limits, the limits are shared by all global plots
                #if (limitsDict2D["limMinXDot"] > min(dataComplete.x)):
                limitsDict2D["limMinXDot"] = min(dataComplete.x)

                limitsDict2D["limMaxXDot"] = max(dataComplete.x)

                limitsDict2D["limMinYDot"] = min(dataComplete.y)

                limitsDict2D["limMaxYDot"] = max(dataComplete.y)
                    
                print("Global 2D dataframes loaded - dot product")

    print("Loading complete")
        
    # Combine list if 3D dot product list has information
    if ((metric == "dot" or metric == "both") and (dimension == 3 or dimension == "both")):
        dataListComplete3D = dataListComplete3D + [-1] + dataListCompleteDot3D

    # Combine list if 2D dot product list has information
    if ((metric == "dot" or metric == "both") and (dimension == 2 or dimension == "both")):
        dataListComplete2D = dataListComplete2D + [-1] + dataListCompleteDot2D

    # Return loaded dataframes
    if (dimension == 2):
        return dataListComplete2D, limitsDict2D
    elif (dimension == 3):
        return dataListComplete3D, limitsDict3D
    else:
        return dataListComplete2D, dataListComplete3D, limitsDict2D, limitsDict3D    
    
def plotGlobal2D(beg, end, dataListComplete, limitsDict, show = True, save = False, saveFolder = None):
    # Creates the global 2D plots with all the words
    # beg              - first day of the interval
    # end              - last day of the interval
    # dataListComplete - list with the complete dataframes with all the words in the model for each plot
    # limitsDictList   - dictionary with the global limits for all plots
    # show             - wether to show plots or not
    # save             - wether to save plots or not
    # saveFolder       - folder to save data
    # return           - none

    # Variable for controlling the change in dataframes based on the cosine similarity to the dataframes based on the dot product
    dot = False

    # Variable for indexes of list that are the same for cosine similarity and dot product data
    repIndex = 0

    # Plot data
    for count, dataComplete in enumerate(dataListComplete):
        # Check if the dataframes changed in metric
        if (not isinstance(dataComplete, pd.DataFrame)):
            dot = True
            repIndex = 0
            continue

        fig, ax = plt.subplots(figsize=(20,20))

        if (not dot):
            fig.suptitle("Metric: Cosine Similarity")
        else:
            fig.suptitle("Metric: Dot Product")

        # Plot the word points
        ax.plot(dataComplete.x, dataComplete.y, color='crimson', marker='o', linestyle='None', markersize=5, alpha=0.40)

        #Label the word points
        for i, label in enumerate(dataComplete.Word):
            plt.annotate(label, (dataComplete.x[i], dataComplete.y[i]),fontsize=17, ha='center')
        
        # Defining Axes
        offset = 0.0 # Change this number to adjust the plot limits in case a little offset is wanted for the limits
        if (not dot):
            ax.set_xlim(limitsDict["limMinX"] - offset, limitsDict["limMaxX"] + offset)
            ax.set_ylim(limitsDict["limMinY"] - offset, limitsDict["limMaxY"] + offset)
        else:
            ax.set_xlim(limitsDict["limMinXDot"] - offset, limitsDict["limMaxXDot"] + offset)
            ax.set_ylim(limitsDict["limMinYDot"] - offset, limitsDict["limMaxYDot"] + offset)

        # Title
        ax.set_title(f"{beg} - {end} (Number of words: {len(dataComplete.index)})")

        # Save plot
        if (save):
            if (not dot):
                plt.savefig(os.path.join(saveFolder, "AllWordsPlot2D.png"))
            else:
                plt.savefig(os.path.join(saveFolder, "AllWordsPlot2D_Dot.png"))

        if (show):
            plt.show()

        repIndex += 1

    return None   
    
def plotGlobal3D(beg, end, dataListComplete, limitsDict, show = True, save = False, saveFolder = None):
    # Creates the global 3D plots with all the words
    # beg              - first day of the interval
    # end              - last day of the interval
    # dataListComplete - list with the complete dataframes with all the words in the model for each plot
    # limitsDictList   - dictionary with the global limits for all plots
    # show             - wether to show plots or not
    # save             - wether to save plots or not
    # saveFolder       - folder to save data
    # return           - none

    # Variable for controlling the change in dataframes based on the cosine similarity to the dataframes based on the dot product
    dot = False

    # Variable for indexes of list that are the same for cosine similarity and dot product data
    repIndex = 0

    # Plot data
    for count, dataComplete in enumerate(dataListComplete):
        # Check if the dataframes changed in metric
        if (not isinstance(dataComplete, pd.DataFrame)):
            dot = True
            repIndex = 0
            continue

        fig = plt.figure(figsize=(20,20))
        ax = fig.add_subplot(projection='3d')

        if (not dot):
            fig.suptitle("Metric: Cosine Similarity")
        else:
            fig.suptitle("Metric: Dot Product")

        # Plot the word points
        ax.plot(dataComplete.x, dataComplete.y, dataComplete.z, color='crimson', marker='o', linestyle='None', markersize=5, alpha=0.40)

        # Defining Axes
        offset = 0.0 # Change this number to adjust the plot limits in case a little offset is wanted for the limits
        if (not dot):
            ax.set_xlim(limitsDict["limMinX"] - offset, limitsDict["limMaxX"] + offset)
            ax.set_ylim(limitsDict["limMinY"] - offset, limitsDict["limMaxY"] + offset)
            ax.set_zlim(limitsDict["limMinZ"] - offset, limitsDict["limMaxZ"] + offset)
        else:
            ax.set_xlim(limitsDict["limMinXDot"] - offset, limitsDict["limMaxXDot"] + offset)
            ax.set_ylim(limitsDict["limMinYDot"] - offset, limitsDict["limMaxYDot"] + offset)
            ax.set_zlim(limitsDict["limMinZDot"] - offset, limitsDict["limMaxZDot"] + offset)

        # Title
        ax.set_title(f"{beg} - {end} (Number of words: {len(dataComplete.index)})")

        # Save plot
        if (save):
            if (not dot):
                plt.savefig(os.path.join(saveFolder,  "AllWordsPlot3D.png"))
            else:
                plt.savefig(os.path.join(saveFolder, "AllWordsPlot3D_Dot.png"))

        if (show):
            plt.show()

        repIndex += 1

    return None    

def top_similiar_words(model, word, top):
    #Finds the words most similar to a specific word
    #model- trained model from which the vocabulary is used
    #word- word to see its most similar words
    #top- the total number of most similar words
    
    print(f"{top} words similar to {word}")
    words = model.wv.most_similar(word, topn=int(top))
    for word in words:
      print(word)
    print()
        
def similarity_2_words(model, word1, word2):
    #Finds the similarity between two words
    #model- trained model from which the vocabulary is used
    #word1- first word to see its similarity
    #word2- he second word to see its similarity with the first one
    
    print(f"The similarity between {word1} and {word2} is {model.wv.similarity(word1, word2)}")
    
    
    
    
    
    
    