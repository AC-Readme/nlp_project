from string import digits
import acquire
import requests
from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd

import re
import unicodedata
import nltk

from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

###################################### Clean Data Function ###############################

def basic_clean(string):
    '''
    Converts text in to ascii to remove special characters, then converts back in to utf-8
    '''
    string = (unicodedata.normalize('NFKD', string.lower())
            .encode('ascii', 'ignore') # ascii to reduce noise
            .decode('utf-8', 'ignore') # decode using utf-8
           )
    return re.sub(r"[^a-z0-9\s]", '', string)

def tokenize(string):
    '''
    This function takes in a string and
    returns a tokenized string.
    '''
    # Create tokenizer.
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    # Use tokenizer
    string = tokenizer.tokenize(string, return_str=True)
    
    return string

def lemmatize(string):
    '''
    This function takes in string for and
    returns a string with words lemmatized.
    '''
    # Create the lemmatizer.
    wnl = nltk.stem.WordNetLemmatizer()
    
    # Use the lemmatizer on each word in the list of words we created by using split.
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    
    # Join our list of words into a string again and assign to a variable.
    string = ' '.join(lemmas)
    
    return string



def remove_stopwords(string, extra_words=['dictionary', 'machine', 'allow', 'directory','file','use','run','using','example','state','via','generate','right','call','end','given','filename','generated','within','however','several','info','dev','necessary','linux','together','bar'], exclude_words=[]):
    '''
    This function takes in a string, optional extra_words and exclude_words parameters
    with default empty lists and returns a string.
    '''
    # Create stopword_list.
    stopword_list = stopwords.words('english')
    
    # Remove 'exclude_words' from stopword_list to keep these in my text.
    stopword_list = set(stopword_list) - set(exclude_words)
    # Add in 'extra_words' to stopword_list.
    stopword_list = stopword_list.union(set(extra_words))
    
    # Split words in string.
    words = string.split()
    
    # Create a list of words from my string with stopwords removed and assign to variable.
    filtered_words = [word for word in words if word not in stopword_list]
    
    # Join words in the list back into strings and assign to a variable.
    string_without_stopwords = ' '.join(filtered_words)
    
    return string_without_stopwords

    
def clean_data(df):
    '''
    This function takes in a dataframe of text, cleans, tokenizes, lemmatizes, and removes stopwords
    from that text, appending each step in the process to the dataframe.  It also appends a list of 
    words from each article as well as the total lenght.  
    '''    
    # Formatt title, makes it easier to read
    df['title'] = df.title.apply(basic_clean)
    df['title'] = df.title.apply(tokenize)
    df['title'] = df.title.apply(lemmatize)
    # Formatts language makes it easier to read
    df['language'] = df.language.apply(basic_clean)
    df['language'] = df.language.apply(tokenize)
    df['language'] = df.language.apply(lemmatize)
    remove_digits = str.maketrans('', '', digits)
    df['language'] = df['language'].str.translate(remove_digits)
    df['language'] = df['language'].str.strip()
    # Formatts repo contents to make them easier to read
    df['text_cleaned'] = df.content.apply(basic_clean)
    df['text_tokenized'] = df.text_cleaned.apply(tokenize)
    df['text_lemmatized'] = df.text_tokenized.apply(lemmatize)
    df['text_filtered'] = df.text_lemmatized.apply(remove_stopwords)
    # Add column with list of words
    words = [re.sub(r'([^a-z0-9\s]|\s.\s)', '', doc).split() for doc in df.text_filtered]
    df = pd.concat([df, pd.DataFrame({'words': words})], axis=1)
    # Adds colum with lenght of word list
    df['doc_length'] = [len(wordlist) for wordlist in df.words]
    return df

####################################### Train, Validate, Test ######################################

def train_validate_test(df):
    
    train_validate, test = train_test_split(df[['language', 'text_filtered', 'words', 'doc_length']], 
                                            random_state = 123,
                                            stratify=df.language, 
                                            test_size=.2)

    train, validate = train_test_split(train_validate, 
                                       random_state = 123,
                                       stratify=train_validate.language, 
                                       test_size=.25)
    return train, validate, test

