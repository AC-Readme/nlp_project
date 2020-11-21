
import pandas as pd
import numpy as np
import requests
from requests import get
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import os

###################################### Get URL Function ################################################

def get_repos(url):

    '''
    This function returns repos associated with a specific page search (www.github.com/)
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
    repos = ['https://github.com' + repo for repo in repos]

    return repos


####################################### URL Import Funciton ############################################


def get_urls():
    '''
    This function collects Github repos when given a URL search page
    '''
    urls = ['https://github.com/freeCodeCamp/freeCodeCamp',
        'https://github.com/Famous/famous',
        'https://github.com/vuejs/vue',
        'https://github.com/kevana/ui-for-docker',
        'https://github.com/facebook/react',
        'https://github.com/ipython/ipython',
        'https://github.com/microsoft/TypeScript-Handbook',
        'https://github.com/airbnb/knowledge-repo',
        'https://github.com/rkern/line_profiler',
        'https://github.com/babel/babel-preset-env',
        'https://github.com/s3tools/s3cmd',
        'https://github.com/zzzeek/sqlalchemy',
        'https://github.com/thunil/TecoGAN',
        'https://github.com/l1ving/youtube-dl',
        'https://github.com/mdo/github-buttons',
        'https://github.com/StephenGrider/ReactNativeReduxCasts',
        'https://github.com/apollographql/apollo',
        'https://github.com/wandb/client',
        'https://github.com/RasaHQ/rasa_core',
        'https://github.com/angular-ui/angular-ui-OLDREPO',
        'https://github.com/urwid/urwid',
        'https://github.com/timqian/star-history',
        'https://github.com/PatrickJS/NG6-starter',
        'https://github.com/knrt10/kubernetes-basicLearning',
        'https://github.com/nature-of-code/noc-book',
        'https://github.com/erikbern/git-of-theseus',
        'https://github.com/dortania/OpenCore-Install-Guide',
        'https://github.com/Kapeli/Dash-User-Contributions',
        'https://github.com/github/docs',
        'https://github.com/StephenGrider/redux-code',
        'https://github.com/fossasia/meilix',
        'https://github.com/StephenGrider/EthereumCasts',
        'https://github.com/newren/git-filter-repo',
        'https://github.com/mateodelnorte/meta',
        'https://github.com/arsaboo/homeassistant-config',
        'https://github.com/IronLanguages/main',
        'https://github.com/StephenGrider/FullstackReactCode',
        'https://github.com/openworm/OpenWorm',
        'https://github.com/apache/nano',
        'https://github.com/jupyterhub/repo2docker',
        'https://github.com/abidrahmank/OpenCV2-Python-Tutorials',
        'https://github.com/Ceruleanacg/Personae',
        'https://github.com/mtdvio/ru-tech-chats',
        'https://github.com/xinntao/EDVR',
        'https://github.com/RubensZimbres/Repo-2017',
        'https://github.com/ipfs-inactive/js-ipfs-http-client',
        'https://github.com/browserpass/browserpass-legacy',
        'https://github.com/boston-dynamics/spot-sdk',
        'https://github.com/sourcerer-io/hall-of-fame',
        'https://github.com/blackorbird/APT_REPORT',
        'https://github.com/creationix/howtonode.org',
        'https://github.com/jennschiffer/make8bitart',
        'https://github.com/wdas/reposado',
        'https://github.com/guyzmo/git-repo',
        'https://github.com/Netflix/repokid',
        'https://github.com/nosarthur/gita',
        'https://github.com/harshjv/github-repo-size',
        'https://github.com/babel/babel-standalone',
        'https://github.com/kevin28520/My-TensorFlow-tutorials',
        'https://github.com/diyhue/diyHue',
        'https://github.com/StephenGrider/rn-casts',
        'https://github.com/headsetapp/headset-electron',
        'https://github.com/StijnMiroslav/top-starred-devs-and-repos-to-follow',
        'https://github.com/techgaun/active-forks',
        'https://github.com/donnemartin/viz',
        'https://github.com/tailwindlabs/tailwindui-vue',
        'https://github.com/GitGuardian/gg-shield',
        'https://github.com/dtschust/redux-bug-reporter',
        'https://github.com/burke-software/django-report-builder',
        'https://github.com/antsmartian/lets-build-express',
        'https://github.com/MicrosoftDocs/visualstudio-docs',
        'https://github.com/earwig/git-repo-updater',
        'https://github.com/OpenSourceTogether/Hacktoberfest-2020',
        'https://github.com/lightaime/deep_gcns_torch',
        'https://github.com/A3M4/YouTube-Report',
        'https://github.com/heroku/heroku-repo',
        'https://github.com/lambdaji/tf_repos',
        'https://github.com/StephenGrider/AdvancedReactNative',
        'https://github.com/lightaime/deep_gcns',
        'https://github.com/StephenGrider/DockerCasts',
        'https://github.com/mappum/gitbanner',
        'https://github.com/declare-lab/conv-emotion',
        'https://github.com/MarkWuNLP/MultiTurnResponseSelection',
        'https://github.com/chriswhong/nyctaxi',
        'https://github.com/18F/analytics-reporter',
        'https://github.com/npmhub/npmhub',
        'https://github.com/kesiev/akihabara',
        'https://github.com/ionic-team/ionic-site',
        'https://github.com/ros/rosdistro',
        'https://github.com/GoogleChromeLabs/tooling.report',
        'https://github.com/rpl/flow-coverage-report',
        'https://github.com/storybook-eol/react-native-storybook',
        'https://github.com/StephenGrider/MongoCasts',
        'https://github.com/kundajelab/deeplift',
        'https://github.com/microsoft/HealthClinic.biz',
        'https://github.com/Redocly/create-openapi-repo',
        'https://github.com/philbooth/complexity-report',
        'https://github.com/bensmithett/webpack-css-example',
        'https://github.com/PhantomInsights/mexican-government-report',
        'https://github.com/googlefonts/Inconsolata',
        'https://github.com/laincloud/lain',
        'https://github.com/auth0/repo-supervisor',
        'https://github.com/weightagnostic/weightagnostic.github.io',
        'https://github.com/jdorn/php-reports',
        'https://github.com/joeldenning/coexisting-vue-microfrontends']

    return urls

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

##### Function to scrape the readme without creating a json file #####

def get_readme_articles_func(urls, cached=False):
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
        #df.to_json('project_readme.json')
    
    return df

