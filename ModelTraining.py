# Script used to create the model. Adapted from the code written by Miguel Bernardo in his master degree thesis "Construction of Geometries Based on Automatic Text Interpretation".

from __future__ import absolute_import, division, print_function
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize

import nltk
nltk.download('punkt')

import multiprocessing
import os
import re
import gensim.models.word2vec as w2v

def word_tokenizer(raw):
    clean = re.sub("[^a-zA-Z]"," ", raw)
    words = word_tokenize(clean)
    return words

def createModel(corpus, saveFolderName, modelName, model=None):
    # Creates and trains a Skip-gram model from a given corpus and saves it in the specified folder
    # corpus         - corpus used to train the model
    # saveFolderName - name of the folder where model is going to be saved
    # modelName      - the name to give the model when it is created
    # model          - pre-existing model to train
    # return         - model after training
   

    file = open(corpus, encoding='utf-8', errors='ignore')
    book = file.read()
    file.close()
    
    raw_days = sent_tokenize(book)
    
    sentences = []
    
    for raw_day in raw_days:
        if len(raw_day) > 0:
            sentences.append(word_tokenizer(raw_day))

    # Tokens Counter
    token_count = sum([len(sentence) for sentence in sentences])
    print("This corpus contains {} tokens.".format(token_count))
    
    # Train The Model
    # If there isn't any pre-existing model, create one
    if (model == None):
        Model = w2v.Word2Vec(
            sg = 1, #Skip-Gram
            workers = multiprocessing.cpu_count(),
            vector_size = 10, #Change if you want a different word vector dimension. Attention: if you change this you need to change the parameters of word_vectors_matrix in DimensionReduction file
            min_count = 1,
            window = 19,
            sample = 1e-4
            )

        Model.build_vocab(sentences)

    else:
        # Else add any new words to the pre-existing model vocabulary
        Model = model
        Model.build_vocab(sentences, update = True)    
    
    
    Model.train(sentences, total_examples=Model.corpus_count,
                           epochs=Model.epochs)
    
    
    # Save The Model
    if not os.path.exists(saveFolderName):
        os.makedirs(saveFolderName)
    
    Model.save(os.path.join(saveFolderName, modelName + ".w2v"))
    
    return model
    
    
    
    
    