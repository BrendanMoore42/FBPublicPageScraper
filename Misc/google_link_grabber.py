"""
author: @BrendanMoore42
date: November 8, 2018

requirements: Selenium, Pandas

This script runs through a google search page and returns all
of the links, dates and descriptions of the link. Only retrieves
the first 100 terms. Enter search terms.

Returns json of data.
"""
# import packages
import time
import numpy as np
import pandas as pd
# import selenium webdriver and exceptions
from selenium import webdriver

# disable chained warnings
pd.options.mode.chained_assignment = None

#terms to search
terms = 'foo fighters'
terms = terms.replace(' ', '+')

url = f'https://www.google.ca/search?q={terms}&num=100'

# store links
links = []

# set random sleep function to randomize link click time
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


def scrape(url):
    """
    Opens google and searches for links with specified search term.
    Scrolls through pages and extracts html links for each blog.

    Async elements may differ but can be sourced from the browser inspector. Where the
    click is intended search for <class='element_here'>.
    """

    # set empty list to append blog data:dictionaries
    page_links = []

    # set webddriver to chrome
    # can be Chrome(), Safari(), Firefox()
    print('Preparing driver...\n')
    driver = webdriver.Chrome()
    random_sleep()

    # retrieve url
    driver.get(url)
    random_sleep()

    # collect links
    print('Getting links...')
    cite_list = driver.find_elements_by_tag_name('cite')
    desc_list = driver.find_elements_by_class_name('st')
    # caption_list = driver.find_elements_by_tag_name('p')
    for cite, desc in zip(cite_list, desc_list):
        x = cite.text
        x = x.split('.com/')[0]
        x = x + '.com'
        y = desc.text

        # print(x, y)

        # set data and append to list
        blog_data = {'blog': x, 'desc': y}
        page_links.append(blog_data)

    # close driver
    print('\n\nClosing driver...')
    driver.close()

    # append page_links to all blogs
    print('Adding to links...\n')
    links.append(page_links)

scrape(url)
print(links)