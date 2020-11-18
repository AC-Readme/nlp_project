
import pandas as pd
import numpy as np
import requests
from requests import get
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import os
####################################### URL Import Funciton ############################################


def get_repos(url):
    '''
    This function collects Github repos when given a URL search page
    '''
    #codeup user agent
    headers = {'User-Agent': 'Codeup Data Science'}

    #url
    response = requests.get(url, headers=headers)

    # using beautiful soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # get link to url
    items = soup.find_all('a', class_='v-align-middle')

    # empty list
    repos = []

    # getting links from page and appending
    for item in items:
        repos.append(item.get('href'))
        #repos.append(item)
    
    #adding github to href
    repos = ['github.com' + repo for repo in repos]

    return repos

######################################## Web Scraping Functions #########################################

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
    creates a list of dictionary of features,converts list to df, and returns df.
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

