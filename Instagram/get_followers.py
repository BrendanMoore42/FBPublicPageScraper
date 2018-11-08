#!/usr/bin/env
"""
author: @BrendanMoore42
date: October 17, 2018

Requirements: Python 3.6+, Selenium, Numpy

Returns Instagram follower/following counts into a pandas dataframe

*Account access and signing in
Instagram Credentials:
    Place username, password in same cred.py

Run in Jupyter Notebook. 
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

#set dataframe
df = pd.read_json('lusbrands_20181029_part_1/messages.json')
def get_instagram_followers(df, verbose=False):
    # set webddriver to chrome
    # can be Chrome(), Safari(), Firefox()
    print('Preparing driver...\n')
    driver = webdriver.Chrome()

    # log in to Facebook Mobile
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
