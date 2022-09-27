import numpy as np
from scipy.linalg import svd
import os
import pathlib
from datetime import datetime
import matplotlib.pyplot as plt

#--------------------------------------- CONFIGURATIONS ----------------------------------------------

# Change these variables if there is an increase in data and more years are added and if the maximum number of years before a checkpoint is reached needs to be bigger
minDay  = '2021-04-05'
maxDay  = '2022-04-04'

#------------------------------------------- CODE ----------------------------------------------------

def apply_svd(folder, beg_day, end_day, reductions):
    #Application of the SVD method to a previously trained Word2Vec model matrix
    #folder- folder of the chosen Word2Vec model 
    #reductions- dimension number for which the reduction will occur
    
    file= os.path.join('Saved Data', folder ,'Mtx_name.npy')
    data = np.load(file)
    
    #Number of rows and columns of the matrix VxN
    rows, columns = data.shape
    print(f"Number of rows is {rows}")
    print(f"Number of columns is {columns}")
    
    for i in reductions:
        
        #Singular-value decomposition
        U, s, VT = svd(data)
        
        # inspect shapes of the matrices
        print(U.shape, s.shape, VT.shape)

        # create m x n Sigma matrix
        S = np.zeros((data.shape[0], data.shape[1]))
        # populate Sigma with n x n diagonal matrix
        S[:data.shape[1], :data.shape[1]] = np.diag(s)
        
        n_component = int(i)
        
        #Recombine matrix S and VT
        S = S[:, :n_component]

        VT = VT[:n_component, :]
        
        #Remake original matrix 
        A = U.dot(S.dot(VT))
        
        np.save(os.path.join('Saved Data', folder, "Mtx_name" +str(i)), A)
        
        
    #Plot the eigenvalues
    x_data= list(range(1, len(s)+1))
    y_data= s
    #print(y_data)
    plt.plot(x_data, y_data, 'go')
    
    if not os.path.exists(os.path.join('Saved Data', folder, 'Graph')):
        os.makedirs(os.path.join('Saved Data', folder, 'Graph'))
        

    plt.savefig(os.path.join('Saved Data', folder, 'Graph','Eigenvalue' +'.png'))
    

#------------------------------------------- Control Communication ----------------------------------------------------        
def validateFunction(choice, type):   
    
    
    # Check if choice is empty
    if (not choice):
        return False, -1
    
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
    
    directory_list=os.listdir(os.path.join(pathlib.Path().absolute(), 'Saved Data'))
    
    if (type == "folder"):

        validationCondition= False
        for i in directory_list:
            if choice == i:
                validationCondition = True

        return validationCondition, choice  

    if (type == "reductions"):
        
        if (not all(x.isnumeric() for x in choice)):
            validationCondition= False
        
        else:
            validationCondition= True                                   
        
        return validationCondition, -1
   
# Loop controling variables
run = True
menu = True

# Menu Loop
while (run):  
    
    # User menu
    if (menu):
        print("Do you want to apply singular-value decomposition?") 
        
        begDay = input(f"Input the first day of the data from {minDay} to {maxDay} in the form YYYY-MM-DD (ex. {minDay}): ")
        
	    # Validate answer - begDay
        validationCondition1, begDay = validateFunction(begDay, "day")

        while (not validationCondition1):
            begDay = input(f"Input is not valid. Must be of the form #YYYY-MM-DD with no space before or after commas or \"-\" and between {minDay} to {maxDay}. Try again: ")
            validationCondition1, begDay = validateFunction(begDay, "day")
        
        print()
        endDay = input(f"Input the last day of the data from {minDay} to {maxDay} in the form YYYY-MM-DD (ex. {maxDay}): ")
        
	    # Validate answer - endDay
        validationCondition2, endDay = validateFunction(endDay, "day")

        while (not validationCondition2):
            endDay = input(f"Input is not valid. Must be of the form #YYYY-MM-DD with no space before or after commas or \"-\" and between {minDay} to {maxDay}. Try again: ")
            validationCondition2, endDay = validateFunction(endDay, "day")
        
        begData = datetime.strptime(begDay, '%Y-%m-%d')
        endData = datetime.strptime(endDay, '%Y-%m-%d')
        
        # Verifie if the first day is before the last
        validationCondition3=True
        if (begData >= endData):
            validationCondition3= False
        
        while (not validationCondition3):
            endDay = input(f"Input is not valid. Must be a day after the first day {begDay}. Try again: ")
            validationCondition3= True
            validationCondition2, endDay = validateFunction(endDay, "day")
            while (not validationCondition2):
                endDay = input(f"Input is not valid. Must be of the form #YYYY-MM-DD with no space before or after commas or \"-\" and between {minDay} to {maxDay}. Try again: ")
                validationCondition2, endDay = validateFunction(endDay, "day")
            endData = datetime.strptime(endDay, '%Y-%m-%d')
            if (begData >= endData):
                validationCondition3= False 
        
        # Create save folder
        
        folder = os.path.join(str(begDay) + "_" + str(endDay))
        
        # Validate answer - folder
        validationCondition4, folder = validateFunction(folder, "folder")

        while (not validationCondition4):
            print()
            print("This model was not created. Try again.") 
            begDay = input(f"Input the first day of the data from {minDay} to {maxDay} in the form YYYY-MM-DD (ex. {minDay}): ")
            
            # Validate answer - begDay
            validationCondition1, begDay = validateFunction(begDay, "day")

            while (not validationCondition1):
                begDay = input(f"Input is not valid. Must be of the form #YYYY-MM-DD with no space before or after commas or \"-\" and between {minDay} to {maxDay}. Try again: ")
                validationCondition1, begDay = validateFunction(begDay, "day")
            
            print()
            endDay = input(f"Input the last day of the data from {minDay} to {maxDay} in the form YYYY-MM-DD (ex. {maxDay}): ")
            
    	    # Validate answer - endDay
            validationCondition2, endDay = validateFunction(endDay, "day")

            while (not validationCondition2):
                endDay = input(f"Input is not valid. Must be of the form #YYYY-MM-DD with no space before or after commas or \"-\" and between {minDay} to {maxDay}. Try again: ")
                validationCondition2, endDay = validateFunction(endDay, "day")
            
            begData = datetime.strptime(begDay, '%Y-%m-%d')
            endData = datetime.strptime(endDay, '%Y-%m-%d')
            
            # Verifie if the first day is before the last
            validationCondition3=True
            if (begData >= endData):
                validationCondition3= False
            
            while (not validationCondition3):
                endDay = input(f"Input is not valid. Must be a day after the first day {begDay}. Try again: ")
                validationCondition3= True
                validationCondition2, endDay = validateFunction(endDay, "day")
                while (not validationCondition2):
                    endDay = input(f"Input is not valid. Must be of the form #YYYY-MM-DD with no space before or after commas or \"-\" and between {minDay} to {maxDay}. Try again: ")
                    validationCondition2, endDay = validateFunction(endDay, "day")
                endData = datetime.strptime(endDay, '%Y-%m-%d')
                if (begData >= endData):
                    validationCondition3= False 
            
            folder = os.path.join(str(begDay) + "_" + str(endDay))
            # Validate answer - folder
            validationCondition4, folder = validateFunction(folder, "folder")
        
        file= os.path.join('Saved Data', folder ,'Mtx_name.npy')
        data = np.load(file)
        rows, columns = data.shape

        print()
        reductions = input("Input which reductions you want to do? Must be the dimension number for which the reduction will occur. If you want more than one reduction, separate them with commas: ")
        
	    # Validate answer - reductions
        reductions = reductions.replace(" ", "").split(",")
        validationCondition5, choice = validateFunction(reductions, "reductions")

        if validationCondition5== True:
            for reduc in reductions:
                if not int(reduc) <= columns  and int(reduc) > 0:
                    validationCondition5= False
   
        while (not validationCondition5):
            reductions = input(f"Input is not valid. Must be numeric values separate by commas, the values must be bigger than 0 and smaller than {columns}. Try again: ")

            reductions = reductions.replace(" ", "").split(",")
            validationCondition5, choice = validateFunction(reductions, "reductions")
            
            if validationCondition5== True:
                for reduc in reductions:
                    if not int(reduc) <= columns  and int(reduc) > 0:
                        validationCondition5= False

        print()  
        apply_svd(folder, begDay, endDay, reductions)
        
        print()
        print("All reductions have been made")
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