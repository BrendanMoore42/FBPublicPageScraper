#!/usr/bin/env
"""
author: @BrendanMoore42
date: October 17, 2018

Requirements: Python 3.6+, Selenium, Numpy

Returns Instagram follower/following counts from list of users

*Account access and signing in
Instagram Credentials:
    Place username, password in same cred.py

To run:
    Navigate to folder or use path,
    In Terminal,
    python main_scraper.py /path/to/list_of_users
"""
#import packages, credentials
import sys
import time
import pickle
import numpy as np
from cred import email, password

#import selenium webdriver and exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#set random sleep function to randomize link click time
def random_sleep(multiplier=1, verbose=False):
    """
    Puts process to sleep for a random amount of time. Can be multiplied for testing,
    and if verbose=True the number will be displayed.
    :multiplier: Extends time by number, default is 1
    :verbose: if True function will display how long it's sleeping
    """
    i = np.random.randint(2, 6)
    i = i * multiplier
    if verbose:
        print(f'sleeping for {i} seconds')
    time.sleep(i)


def followers_to_int(text):
    """
    Splits followers and numbers
    :text: input text ex. '1.5m followers'
    :return: int: value ex.
    """
    #split text
    text = text.split(' ')[0]
    #if number has period or letter, splits and return rounded count
    if text[-1] == 'm':
        if '.' in text:
            text = text.replace('.', '')
        text = text[:-1] + '00000'
        text = int(text)
    elif text[-1] == 'k':
        text = text[:-1] + '000'
        text = int(text)

    text = int(text)
    return text

def main():
    """
    Opens a browser instance and navigates to target pages, extracting users and comments.
    Each page is placed into a dictionary then pickled as a list of all pages, into the
    same directory as the script run.

    Async elements may differ but can be sourced from the browser inspector. Where the
    click is intended search for <class='element_here'>.

    :args[1]: file containing list of ID's
              example - ig_account_ids.txt
    """

    #set list of dictionaries for data export
    page_data = {}
    user_list = []

    #set webddriver to chrome
    #can be Chrome(), Safari(), Firefox()
    print('Preparing driver...\n')
    driver = webdriver.Chrome()

    #log in to Instagram
    url = 'https://www.instagram.com'
    url = 'https://www.instagram.com/accounts/login/'
    driver.get(url)
    random_sleep()

    #log in
    email_input = driver.find_elements_by_css_selector('form input')[0]
    email_input.send_keys(email)
    password_input = driver.find_elements_by_css_selector('form input')[1]
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)
    random_sleep()

    for url in users:

        url = f'https://www.instagram.com/{url}'
        driver.get(url)
        random_sleep()

        #get followers
        user_info = driver.find_elements_by_css_selector('ul li a')
        followers = followers_to_int(user_info[0].text)
        follows = followers_to_int(user_info[1].text)
        #print(followers, follows)

        page_data = {'user': url,
                     'followers': followers,
                     'follows': follows}
        
        random_sleep()
        

if __name__ == '__main__':
    main()
