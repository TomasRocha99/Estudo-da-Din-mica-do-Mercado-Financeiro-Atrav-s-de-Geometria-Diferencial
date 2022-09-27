# Script used to reduce the dimensions of the data created. Adapted from the code written by Miguel Bernardo in his master degree thesis "Construction of Geometries Based on Automatic Text Interpretation". 

from __future__ import absolute_import, division, print_function
import numpy as np
import os
import gensim.models.word2vec as w2v
from sklearn.manifold import TSNE

def dotProduct(row1, row2):
    # Calculates the dot product between 2 values
    # row1   - first value for the dot product
    # row2   - second value for the dot product
    # return - dot product between row1 and row2

    return np.dot(row1, row2)

def reduceDimension(model, saveFolderName, dimension, metric):
    # Makes a dimension reduction with t-SNE based on the arguments given
    # model          - model to be reduced
    # saveFolderName - name of the folder to save the data and get the data
    # dimension      - the dimension of the reduced space, either 2 or 3
    # metric         - the metric to be used by the t-SNE algorithm in the dimension reduction, either "cosine" or "dotProduct"
    # return         - matrix with the reduced coordinates

    # Information for the user
    print("Model loaded")

    # Check if there is already a matrix with all words from the model, if not make one
    if (not os.path.exists(os.path.join(saveFolderName, "Mtx_name.npy"))):

        # Vocabulary length
        vocab_len = len(model.wv)
        print("Vocabulary length is ", vocab_len)
        
        # Define Matix
        word_vectors_matrix = np.ndarray(shape=(vocab_len, 10), #If you change vector_size, change here too
                                                 dtype='float64')
        word_list = []
        i = 0
        
        # Fill the Matix
        for word in model.wv.key_to_index:
            word_vectors_matrix[i] = model.wv[word]
            word_list.append(word)
            i += 1
            if i == vocab_len:
                break

        # Save Matrix
        np.save(os.path.join(saveFolderName, "Mtx_name"), word_vectors_matrix)

    else:
        # Else load the pre-existing matrix
        word_vectors_matrix = np.load(os.path.join(saveFolderName, "Mtx_name.npy"))
    
        
    if (dimension == 2):
        # Compress the word vectors into a 2D space

        # Define wich metric to be used
        if (metric == "cosine"):
            tsne = TSNE(n_components = 2, random_state = 0, metric=metric)
            matrixName = "Mtx_2d_TSNE"
        elif (metric == "dotProduct"):
            tsne = TSNE(n_components = 2, random_state = 0, metric=dotProduct)
            matrixName = "Mtx_2d_TSNE_dot"

        word_vectors_matrix_2d = tsne.fit_transform(word_vectors_matrix)

        # Save 2D Matrix
        np.save(os.path.join(saveFolderName, matrixName), word_vectors_matrix_2d)

        return word_vectors_matrix_2d

    if (dimension == 3):
        # Compress the word vectors into 3D space

        # Define wich metric to be used
        if (metric == "cosine"):
            tsne = TSNE(n_components = 3, random_state = 0, metric=metric)
            matrixName = "Mtx_3d_TSNE"
        elif (metric == "dotProduct"):
            tsne = TSNE(n_components = 3, random_state = 0, metric=dotProduct)
            matrixName = "Mtx_3d_TSNE_dot"

        word_vectors_matrix_3d = tsne.fit_transform(word_vectors_matrix)

        # Save 3D Matrix
        np.save(os.path.join(saveFolderName, matrixName), word_vectors_matrix_3d)

        return word_vectors_matrix_3d
    
    
    