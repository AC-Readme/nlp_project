
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
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.tree import DecisionTreeClassifier


######################## Function: README predict ########################
def make_soup(url):
    '''
    This helper function takes in a url and requests and parses HTML
    returning a soup object.
    '''
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_readme_articles(urls, cached=False):
    '''
    This function takes in a list of GitHub Repo urls and a parameter
    with default cached == False which scrapes the title, text, and language for each url, 
    creates a list of dictionary features, converts list to df, and returns df.
    If cached == True, the function returns a df from a json file.
    '''
    if cached == True:
        df = pd.read_json('project_readme.json')
        
    # cached == False completes a fresh scrape for df     
    else:

        # Create an empty list to hold dictionaries
        text = []

        # Loop through each url in our list of urls
        for url in urls:

            # Make request and soup object using helper
            soup = make_soup(url)

            # Save the title of each repo in variable title
            title = soup.select('h1', class_="Label Label--outline v-align-middle")[0].text

            # Save the text in each repo to variable text
            content = soup.select('article', class_="markdown-body entry-content container-lg")[0].text
            
            # Save the language of each repo in variable language
            language = soup.select('li.d-inline:nth-child(1) > a:nth-child(1)')[0].text

            # Create a dictionary holding the title and content for each blog
            repo = {'title': title, 'content': content, 'language': language}

            # Add each dictionary to the articles list of dictionaries
            text.append(repo)
            
        # convert our list of dictionaries to a df
        df = pd.DataFrame(text)

        # Write df to a json file for faster access
        df.to_json('project_readme.json')
    
    return df

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

def predict_readme(url):
    '''
    This function takes in a url and scrapes the README data to be cleaned and prepped.
    It is then run thru a decision tree classifier with the TF-IDF as its feature
    to determine the repository language'''
    
    # scrapes the data
    df = get_readme_articles(url,cached=False)
    # cleans the data
    df = clean_data(df)
    
    # using TF-IDF as a feature
    tfidf = TfidfVectorizer(stop_words='english', min_df=20, 
                                 ngram_range=(1,2), 
                                 binary=True)
    # fitting on the entire dataframe
    tfidf.fit(df.text_filtered)
    y = df.language
    X = tfidf.transform(df.text_filtered)

    # define classifier
    tree = DecisionTreeClassifier(max_depth=4, random_state=123)
    tree.fit(X, y)
    # transforming the feature to the single url
    X = tfidf.transform(df.text_filtered)
    y = df.language
    # predicting the language of the single url
    prediction = tree.predict(X)
    print('This function predicts that the language of the selected repository is:',prediction)