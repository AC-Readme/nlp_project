# NLP Classification Project

### Author: Corey Solitaire, Angel Gomez

![](https://portswigger.net/cms/images/54/14/6efb9bc5d143-article-190612-github-body-text.jpg)

## Project Description: 
- Use web scraping to build, fit, and train a classification model to predict the primary language of a GitHub repository.  

## Project Goals:
1. Build a web scraper that extracts the contents of 100 GitHub repository README.md texts as well as the primary language of the repos.
2. Use this data to build a classification model to predict the primary langue of the repository
3. Develop a function that will take in the text of a README file, and use that data to predict the programming language.

## Executive Summary: 

**Project Summary:**   
The purpose of this project was to utilize web scraping to predict the primary programing language of GitHub repository README texts. A function was developed that takes in a list of GitHub URL addresses and collects README text data, as well as the repository's primary programing language. After texts were collected, a classification model was developed that leveraged language specific feature selection tools to accurately predict the primary programing language of the repository. Finally, several functions were combined to produce a single function called predict_readme( ) that takes in a GitHub repository URL and returns a prediction of primary program language (Python/Javascript)

**Background:**   
Web scraping is the process of collecting structured web data in an automated fashion. In this project, we leveraged the speed in automated data collection to collect data from 105 GitHub repository README texts. To extract the necessary information, we developed a function based on a popular natural language processing (NLP) library known as Beautiful Soup. This tool allows us to identify and extract information on websites, which was then stored in a large file that made up the body (corpus) of our project.

**Process:**   
While exploring the corpus, several trends were observed. While several words were specific to individual repositories, the vast majority of words which were observed were common in both. Also, initial hypothesis testing suggested a statistically significant difference between the length of repository based on its primary programing language. The large number of common words and the significant difference between document length led us to examine the inverse document frequency of these common words. Inverse document frequency (IDF) is defined as a measure of the number of documents in which a particular word will appear. The 29 most common words were found in over 20% of all documents. After our initial round of testing struggled to accurately predict Python repositories, the 29 common words were removed.

**Results and Conclusions:**   
Modeling produced an 85% improvement over baseline using a Bag of Words (BOW) feature selection tool fit to logistic regression model. Initial rounds of modeling struggled to predict Python repositories. However, after the common words were removed the model's accuracy did not significantly change over train, validate, test. There exists that regression models may not be the best tool to predict programing language in the dataset due to the success observed using alternate decision tree models in our final function predict_readme( ).

**Next Steps:**   
More Data - This dataset represented a relatively small sample of all GitHub repositories. A more robust dataset would provide a way to evaluate model performance over numerous trials while providing the model with a wider variety of repository README.md data.

New Models - In this project, we evaluated two different feature selection tools (BOW and TF-IDF) using a single logistic regression model. There exists the possibility that other models may lend themselves better to classifying NLP data.

Explore Other Languages - We designed our current model to classify between two primary text languages, Python and Javascript. It would be interesting to explore how the model's performance would be affected by adding more languges. By grouping all other languages together in a feature known as 'other' would we be able to get a better signal on a single language?   

## Instructions for Replication

Files are located in Git Repo [here](https://github.com/AC-Readme/nlp_project)


## Data Dictionary
  ---                  ---
| **Terms**           | **Definition**                                                                          |
| ---                 | ---                                                                                     |
| document            | A single observation, like the body of an email                                         |
| corpus              | Set of documents, dataset, sample, etc                                                  |
| tokenize            | Breaking text up into linguistic units such as words or n-grams                         |
| lemmatize           | Return the base or dictionary form of a word, which is the lemma                        |
| stopwords           | Commonly used word (such as “the”, “a”, “an”, “in”) that are ignored                    |
| Beautiful Soup      | A Python library for pulling data out of HTML and XML files                             |
| web scraper         | A data science technique used for extracting data from websites                         |
| programing language | A set of commands that a computer understands                                           |
| TF                  | Term Frequency; how often a word appears in a document                                  |
| IDF                 | Inverse Document Frequency; a measure based on in how many documents will a word appear |
| TF-IDF              | A holistic combination of TF and IDF                                                    |
  ---                  ---                                                    
***

## Audience:
- General

## Setting:
- Informal

## Workflow:
![](https://github.com/CSolitaire/zillow_cluster_project/blob/main/pipeline%20copy.jpg)
