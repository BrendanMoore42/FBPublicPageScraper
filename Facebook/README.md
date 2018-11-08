# Facebook Public Page Scraper
Extracting comments from a public page typically requires a token granted through Facebook's Graph API--this can be denied or otherwise take time in getting approved. This script uses pre-authorized analytics access on a public page to parse through pages to extract users and comments data <i>without</i> a token.  

### Requirements & Packages
* Tested on OSX with Chrome() webdriver
* Python 3.6+
* Selenium, Numpy
* Analyst Access on Public Page

#### First Steps 
Acquire list of unique page ID's through Facebook and place into .txt file. 

#### Running the script
In terminal, go to target directory, activate virtual environment or run:

    $ python main_scraper.py /path/to/file.txt
 
Script will show # of files to parse, page ID and which step is complete. Page load timeouts or errors will force the loop onto the next page. Pickles files as dictionary output. 
