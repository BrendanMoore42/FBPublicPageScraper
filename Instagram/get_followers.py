#!/usr/bin/env
"""
author: @BrendanMoore42
date: October 17, 2018

Requirements: Python 3.6+, Selenium, Numpy

Search through your Instagram direct messages data to set user information into a dataframe.

*Account access and signing in
Instagram Credentials:
    Place username, password in same cred.py

Can be run in Jupyter Notebook, or from ide if necessary. 
"""
#import packages
import sys
import time
import pickle
import numpy as np
import pandas as pd
from cred import email, password
#import selenium packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#disable chained warnings
pd.options.mode.chained_assignment = None 

#set dataframe from dataframe
df = pd.read_json('your_ig_account/messages.json')

#put all users into a set to remove duplicates
top_dms = set()
#loop through df for any users that have a story share
for i, user in enumerate(df.conversation):
    for j in user:
        if "story_share" in j:
            top_dms.add(j['sender'])
            
#display how many users shared a story 
print(f'{len(top_dms)} users mentioned you a story.')

#collect names to remove from the set
to_remove = ['any_account', 'you_dont_want', 'put_here']
#remove unwanted accounts
top_dms = [x for x in top_dms if x not in to_remove]

#create and set dataframe to prepare for extraction
dfs = pd.DataFrame(top_dms, columns=['Users'])
dfs['Posts'], dfs['Followers'], dfs['Follows'] = 0,0,0

#set random sleep function to randomize link click time
def random_sleep(multiplier=1, verbose=False):
    """
    This function goes between various actions to give the browser time to load and
    prepare html for parsing.
    :multiplier: Extends time by number, default is 1
    :verbose: if True function will display how long it's sleeping
    """
    i = np.random.randint(2, 6)
    i = i * multiplier
    if verbose:
        print(f'sleeping for {i} seconds')
    time.sleep(i)

#converts IG strings to true ints
def followers_to_int(text):
    """
    Splits followers and numbers
    :text: input text ex. '1.5m followers'
    :return: int: value ex.
    """
    #split text
    text = text.split(' ')[0]
    #if number has period or letter, splits and return rounded count
    try:
        if text[-1] == 'm':
            if '.' in text:
                text = text.replace('.', '')
                text = text[:-1] + '00000'
            else: 
                text = text.replace('m', '000000')
            text = int(text)
        elif text[-1] == 'k':
            if '.' in text:  
                text = text.replace('.', '')
                text = text[:-1] + '00'
            else:
                text = text = text.replace('k', '000')
            text = int(text)
        elif ',' in text:
            text = text.replace(',', '')
            text = int(text)
        text = int(text)
    except (IndexError, ValueError):
        text = 0
    return text

#loops through followers in json and sets all into a dataframe
def get_instagram_followers(df, verbose=False):
    # set webddriver to chrome
    # can be Chrome(), Safari(), Firefox()
    print('Preparing driver...\n')
    driver = webdriver.Chrome()

    # log in to Instagram
    # url = 'https://www.instagram.com'
    url = 'https://www.instagram.com/accounts/login/'
    driver.get(url)
    random_sleep()

    # log in
    email_input = driver.find_elements_by_css_selector('form input')[0]
    email_input.send_keys(email)
    password_input = driver.find_elements_by_css_selector('form input')[1]
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)
    random_sleep()

    # set timeout if page hangs for too long
    driver.set_page_load_timeout(60)

    for i, user in enumerate(df.Users):
        # prints number of users left if verbose=True
        if verbose and i % 250 == 0:
            print(f'\n{i} Users scraped...\n')

        # only grabs users thave have not been searched yet
        if df.Followers.iloc[i] < 0:
            continue
        else:
            try:
                # navigate to users page
                url = f'https://www.instagram.com/{user}'
                driver.get(url)
                random_sleep(verbose=True)

                # get followers
                user_info = driver.find_elements_by_css_selector('ul li')
                # grab posts, followers and follow counts, add to dataframe
                df.Posts.iloc[i] = followers_to_int(user_info[0].text)
                df.Followers.iloc[i] = followers_to_int(user_info[1].text)
                df.Follows.iloc[i] = followers_to_int(user_info[2].text)

                print(user + ' complete!\n')
                continue
                # random_sleep()
            except TimeoutError:
                df.Posts.iloc[i] = -1
                df.Followers.iloc[i] = -1
                df.Follows.iloc[i] = -1
                continue

    print('Done!')
    driver.close()
    
#run IG script
get_instagram_followers(dfs)

#save to csv
dfs.to_csv('file_name_here.csv')
