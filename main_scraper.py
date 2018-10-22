#!/usr/bin/env
"""
author: @BrendanMoore42
date: October 17, 2018

Requirements: Python 3.6+, Selenium, Numpy

Retrieve Facebook comments with page ID's. ID's can be obtained
from downloading page data via Facebook's analytic accounts.

This method does not require token access and deploys through the
mobile browser for static page views.

*If using account to access and sign in:
Credentials:
    Place in same folder cred.py with username, email and facebook id.
    Facebook ID is static and can be found on mobile version of public page:
    ex. https://mobile.facebook.com/story.php?story_fbid={page}&id={FACEBOOK_ID}&anchor_composer=false

To run:
    Navigate to folder or use path,
    In Terminal,
    python main_scraper.py /path/to/file
"""
#import packages, credentials
import sys
import time
import pickle
import numpy as np
from cred import email, password, facebook_id

#import selenium webdriver and exceptions
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementNotVisibleException

#set FB parameters account file name
fb_account = 'ACCOUNT NAME HERE'

fid = facebook_id

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

def main(args):
    """
    Opens a browser instance and navigates to target pages, extracting users and comments.
    Each page is placed into a dictionary then pickled as a list of all pages, into the
    same directory as the script run.

    Async elements may differ but can be sourced from the browser inspector. Where the
    click is intended search for <class='element_here'>.

    :args[1]: file containing list of ID's
              example - fb_account_ids.txt
    """
    file = args[1]

    #set list of dictionaries for data export
    page_data = {}
    page_data_list = []

    #full id list
    with open(file, 'r') as f:
        ids = f.readlines()

    print(f'Looping through {len(ids)} pages...\n')

    #set webddriver to chrome
    #can be Chrome(), Safari(), Firefox()
    print('Preparing driver...\n')
    driver = webdriver.Chrome()

    # #navigate to mobile facebook
    # url = 'https://mobile.facebook.com'
    # driver.get(url)
    # random_sleep()
    #
    # #log in
    # x = driver.find_element_by_id('m_login_email')
    # x.send_keys(email)
    # random_sleep()
    #
    # y = driver.find_element_by_id('m_login_password')
    # y.send_keys(password)
    # random_sleep()
    #
    # #login button
    # z = driver.find_element_by_id('u_0_5')
    # z.click()
    # random_sleep()
    #
    # #click 'not now' button
    # xpath = '//*[@id="root"]/div[1]/div/div/div[3]/div[1]/div/div/a'
    # w = driver.find_element_by_xpath(xpath)
    # w.click()
    # random_sleep()


    #loop through ID's to grab comments
    print('Starting:\n')
    for i, page in enumerate(ids):
        """
        For every page, selenium obtains the caption, users, and comments. Comments will need to be
        expanded to view all replies. After those elements are clicked, the user:comment data 
        is added to the data dictionary along with id# and page caption. 
        """
        #page ID
        print(f'#{i}\tID: {page}')

        #navigate to new url
        print('Get Url...')
        new_url = f'https://mobile.facebook.com/story.php?story_fbid={page}&id={fid}&anchor_composer=false'
        driver.get(new_url)
        random_sleep(2)

        #set dictionary key:value pairs
        page_data = {'id': page}

        #set data variables
        captions, user_list = [], []

        #grab captions
        print('Get Caption...')
        try:
            caption_list = driver.find_elements_by_tag_name('p')
            for cap in caption_list:
                x = cap.text
                captions.append(x)
        except:
            print('No caption...')

        #set captions to page data dictionary
        page_data['caption'] = captions
        random_sleep()

        """
        Comments Loop:
        
        On page, the following loop clicks through  all the 
        async elements that expand comments. When no more elements 
        are present, the loop breaks. 
        
        Load times:
        
        Page may hang due to the view comment async element not loading, 
        load_timeout is the length of time you want to wait until skipping 
        to the next page. 
        """
        print('Expanding comments...')
        driver.set_page_load_timeout(10)
        while True:
            try:
                driver.find_element_by_class_name("async_elem").click()
                #time.sleep()
            except (TimeoutException, StaleElementReferenceException, ElementNotVisibleException, NoSuchElementException) as e:
                #print(e)
                break
        #reset load timeout for other functions
        driver.set_page_load_timeout(120)

        #grab user name and user comment
        random_sleep()
        print('Get users, comments...')
        while True:
            try:
                #element is container that holds user's post
                users = driver.find_elements_by_class_name("_2b06")
                random_sleep()
                break
            except (ElementNotVisibleException, NoSuchElementException) as e:
                #print(e)
                break

        #append to list username and comments
        for user in users:
            x = user.text
            user_list.append(x)

        #add user comments to page data
        page_data['comments'] = user_list

        #add page to list, loop back
        print('Page complete, sleeping...\n')
        page_data_list.append(page_data)
        random_sleep()

        #backup every n=50 pages in case error
        if i > 0 and i % 50 == 0:
            print(f'\nBacking up {i} pages in data list...')
            with open(f'{fb_account}_data_backup_{i}_{page}.pkl', 'wb') as f:
                pickle.dump(page_data_list, f)
                print('Resuming loop...')
            continue

    #pickle for export
    print('Done!')
    print('\n\nPickling file...')
    with open(f'{fb_account}_data.pkl', 'wb') as f:
        pickle.dump(page_data_list, f)
        print('Pickle successful!')

    print('\n\nClosing driver...')
    driver.close()

if __name__ == '__main__':
    main(sys.argv)
