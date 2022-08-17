# Movie info scraper 🎬🎈🍿

This script scraps movie info from [yts.mx](https://yts.mx/browse-movies)

This script scraps
* Movie covers
* Movie info (name, rating release year, genre)

## Options
You can provide several inputs to scrap info for specific movies
* Language: 1: All  2: English  3: French  4: Italian  5: Japanese  6: Chinese  7: Korean
* Genre: 1: All  2: Action  3: Animation  4: Comedy  5: Drama  6: Horror  7: Sci-Fi
* Order by: 1: Downloads  2: Seeds  3: Likes  4: Rating  5: Year


## How to use
Just run the script with python SCRIPT_NAME command

## How this script works
The script creates a folder on desktop with the name 'yts_scrap' and all the content is stored in this folder (images and csv file)

## Sample Scraped Data
I have added sample scraped data so you can see what this script scrapes [Here](https://github.com/junaid9211/Web-Scraping/tree/main/1.%20Movie%20info%20scaper/sample%20scraped%20data)

## Dependencies
You will need to install the following libraries for the script to work
* requests
* bs4
* lxml
