import time
import os

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'
          }
# EXAMPLE_PROXY = {"https": "https//59.110.7.190:1080"}
DOCUMENT = "anime.txt"
CHROMEDRIVER_PATH = "/"  # This file's location
REVISION_DATE = "2019-June-11"
TOTAL_RESOURCE_COUNT = 3

# open the file and grab the urls
urls = []
animeNames = []
resourceCount = 0

# Grab every url with 'http' in it and extract anime name from the url
file = open(DOCUMENT, "r")
print("INFO: Compiling URLs...")
lines = file.readlines()
file.close()
for line in lines:
    for word in line.split(" "):
        if word.startswith("http"):
            # url must match regex
            pattern = "https://www.[\\S]"  # Don't need to re.compile(pattern) because I'm only using it here
            urls.append(word)
            # save anime name
            # if there is a slash at the end of the url, remove it
            if (word[len(word)-1] == '/'):
                word = word[:-1]
            k = word.rfind("/")
            word = word[k + 1:]
            animeNames.append(word)
            print("Found anime " + word)

i = 0
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=options)  # Replace with .Firefox(), or with the browser of your choice

for url in urls:

    resourceCount = 0
    # Cut off number in anime name & remove all newlines
    #animeNames[i] = animeNames[i][animeNames[i].find("-") + 1:].replace('\n', '')
    print("INFO: Downloading image and page data for " + animeNames[i] + "...")
    browser.get(url)  # Navigate to the page
    time.sleep(1)  # IMPORTANT: Keep this at least one second to not get flagged as a bot

    resourcePath = "anime/" + animeNames[i] + "/"
    try:
        os.makedirs(resourcePath + "images/")  # <-- Throws exception

        # Get the box image source
        element = browser.find_element_by_xpath('//*[@id="app"]/div[3]/div/div[1]/div[2]/div/div[1]/div/img')
        boxArtUrl = element.get_attribute('src')

        try:
            # Download the image
            #urlretrieve(boxArtUrl, resourcePath + "images/" + animeNames[i] + "-box-art.png") This is no good for websites protecting against DDoS attacks using things like cloudflare
            # https://stackoverflow.com/questions/49530566/download-an-image-using-selenium-webdriver-in-python
            # Use selenium to download the image by passing the cookies to a requests session, bypassing logins and DDoS protection systems
            session = requests.session()
            session.headers.update(HEADER)
            for cookie in browser.get_cookies():
                c = {cookie['name']: cookie['value']}
                session.cookies.update(c)
            resource = session.get(boxArtUrl, allow_redirects=True)
            open(resourcePath + "images/" + animeNames[i] + "-box-art.jpg", 'wb').write(resource.content)

            resourceCount += 1
        except ValueError:
            # Failed to download image (may not exist)
            print("No box image found...")

        # Get the background/cover image source
        element = browser.find_element_by_xpath('//*[@id="app"]/div[3]/div/div[1]/div[1]')
        rawCoverImageUrl = element.get_attribute('style')
        startIndex = rawCoverImageUrl.find("http")
        endIndex = len(rawCoverImageUrl) - rawCoverImageUrl.find(".jpg") - 4
        coverImageUrl = rawCoverImageUrl[startIndex:-endIndex]
        try:
            # Download the image
            #urlretrieve(coverImageUrl, resourcePath + "images/" + animeNames[i] + "-cover.jpg")
            session = requests.session()
            session.headers.update(HEADER)
            for cookie in browser.get_cookies():
                c = {cookie['name']: cookie['value']}
                session.cookies.update(c)
            resource = session.get(coverImageUrl, allow_redirects=True)
            open(resourcePath + "images/" + animeNames[i] + "-cover.jpg", 'wb').write(resource.content)
            resourceCount += 1
        except ValueError:
            # Failed to download image (may not exist)
            print("No background found...")

        dataFile = open(resourcePath + "data.txt", "w+")
        rankingsList = []
        rankings = browser.find_elements_by_xpath("//*[@class='rank-text']")
        for item in rankings:
            rankingsList.append(item.text)
            dataFile.write(item.text + "\n")

        listData = []
        data = browser.find_elements_by_xpath("//*[@class='data-set']")
        for item in data:
            listData.append(item.text)
            try:
                dataFile.write(item.text + "\n")
            except UnicodeEncodeError:
                print() #Ignore - Probably encountered Japanese text

        lstData = []
        data = browser.find_elements_by_xpath("//*[@class='data-set data-list']")
        for item in data:
            lstData.append(item.text)
            dataFile.write(item.text + "\n")

        tagsList = []
        tags = browser.find_elements_by_xpath("//*[@class='tag']")
        for item in tags:
            tagsList.append(item.text)
            dataFile.write(item.text + "\n")
        dataFile.close()
        resourceCount += 1

        if resourceCount == 3:
            print("Successfully downloaded all resources for " + animeNames[i])
    except FileExistsError:
        print("ERROR: " + resourcePath + " already exists; skipped.")
    except NoSuchElementException:
        # Selenium can't find an element
        print("ERROR: Can't find element. Are you using an anime page from anilist.co?")

    print("\n")
    # Cycle to next anime name
    i += 1

browser.close()
