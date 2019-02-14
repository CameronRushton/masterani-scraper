import time
import os
import re
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
# EXAMPLE_PROXY = {"https": "https//59.110.7.190:1080"}
DOCUMENT = "anime.txt"
CHROMEDRIVER_PATH = "/"  # This file's location
REVISION_DATE = "2019-Feb-10"
TOTAL_RESOURCE_COUNT = 3

# open the file and grab the urls
urls = []
animeNames = []
resourceCount = 0

# TODO: Have this data taken dynamically from the genres list on site
genres = ["Action", "Adventure", "Cars", "Comedy",
           "Dementia", "Demons", "Drama", "Ecchi",
           "Fantasy", "Game", "Harem", "Historical",
           "Horror", "Josei", "Kids", "Magic",
           "Martial Arts", "Mecha", "Military", "Music",
          "Mystery", "Parody", "Police", "Psychological",
          "Romance", "Samurai", "School", "Sci-Fi",
          "Seinen", "Shoujo", "Shoujo Ai", "Shounen",
          "Shounen Ai", "Slice of Life", "Space", "Sports",
          "Super Power", "Supernatural", "Thriller", "Vampire",
          "Yaoi", "Yuri"]

# Grab every url with 'http' in it and extract anime name from the url
file = open(DOCUMENT, "r")
print("INFO: Compiling URLs...")
lines = file.readlines()
file.close()
for line in lines:
    for word in line.split(" "):
        if word.startswith("http"):
            # url must match regex
            pattern = "https://www.masterani.me/anime/info/[\\S]"  # Don't need to re.compile(pattern) because I'm only using it here
            if not re.match(pattern, word):
                print("ERROR: Invalid URL " + word)
                continue
            urls.append(word)
            # save anime name
            k = word.rfind("/")
            animeNames.append(word[k + 1:])

i = 0
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=options)  # Replace with .Firefox(), or with the browser of your choice

for url in urls:

    resourceCount = 0
    # Cut off number in anime name & remove all newlines
    animeNames[i] = animeNames[i][animeNames[i].find("-") + 1:].replace('\n', '')
    print("INFO: Downloading image and page data for " + animeNames[i] + "...")
    browser.get(url)  # Navigate to the page
    time.sleep(1)  # IMPORTANT: Keep this at least one second to not get flagged as a bot

    resourcePath = "anime/" + animeNames[i] + "/"
    try:
        os.makedirs(resourcePath + "images/")  # <-- Throws exception

        # Get the box image source
        element = browser.find_element_by_xpath('//div[@class="cover"]/img')
        boxArtUrl = element.get_attribute('src')
        try:
            # Download the image
            urlretrieve(boxArtUrl, resourcePath + "images/" + animeNames[i] + "-box-art.png")
            resourceCount += 1
        except ValueError:
            # Failed to download image (may not exist)
            print("No box image found...")

        # Get the background/cover image source
        element = browser.find_element_by_xpath('//div[@id="head"]')
        rawCoverImageUrl = element.get_attribute('style')
        startIndex = rawCoverImageUrl.find("http")
        endIndex = len(rawCoverImageUrl) - rawCoverImageUrl.find(".jpg") - 4
        coverImageUrl = rawCoverImageUrl[startIndex:-endIndex]
        try:
            # Download the image
            urlretrieve(coverImageUrl, resourcePath + "images/" + animeNames[i] + "-cover.jpg")
            resourceCount += 1
        except ValueError:
            # Failed to download image (may not exist)
            print("No background found...")

        # get stats for ratings, view counts, genre tags & other js
        elements = browser.find_elements_by_xpath("//*[@class='item']")
        writeData = False
        dataFile = open(resourcePath + "data.txt", "w+")
        dataFile.write("GENRES\n")
        for element in elements:
            try:
                if genres.index(element.text) != -1:  # If a genre is found, write it
                    dataFile.write(element.text + "\n")
            except ValueError:
                print()  # Do nothing
            if element.text == "PRIVACY":  # We're done at this point
                break
            if element.text.find("AVG. SCORE") != -1:  # Write the rest of the elements
                writeData = True
            if writeData:
                dataFile.write(element.text + "\n")
        resourceCount += 1
        dataFile.close()
        if resourceCount == 3:
            print("Successfully downloaded all resources for " + animeNames[i])
    except FileExistsError:
        print("ERROR: " + resourcePath + " already exists; skipped.")
    except NoSuchElementException:
        # Selenium can't find an element (probably because the web page given is not a masterani.me anime page)
        print("ERROR: Can't find element. Are you using an anime page from masterani.me?" +
              "Hint: Should look like 'https://www.masterani.me/anime/info/anime-name'" +
              "If you think the page may have changed since " + REVISION_DATE + ", contact Shoyu")

    print("\n")
    # Cycle to next anime name
    i += 1

browser.close()
