import requests
import bs4
import csv
import time
import os
import re
import math
import datetime
import threading


def return_log(**kwargs):
    x = str(datetime.datetime.now())
    x = x.split('.')[0].split()
    text= f'''{kwargs['pages']} page(s) from {kwargs['link']} were scraped
    
Options Choosen
    Genre: {kwargs['options'][0]}
    Language: {kwargs['options'][1]}
    Order by: {kwargs['options'][2]}
    Covers scrapped?: {kwargs['covers']}
    
Script ran on {x[0]} at {x[1]}

Script created by Muhammad Junaid
    '''
    return text

def movie_details(m):
    name = m.select('.browse-movie-title')[0].text
    year = m.select('.browse-movie-year')[0].text
    rating = m.select('.rating')
    
    if rating == []:
        rating = 'no rating'
    else:
        rating = m.select('.rating')[0].text.split('/')[0]
    
    genres = [g.text for g in m.select('h4')[1:]]
    genres = ' '.join(genres)
    
    return [name, year, rating, genres]


def save_cover(path, m):
    
    link = m.select('img')[0]['src']
    unformated_name = m.select('.browse-movie-title')[0].text
    name = re.findall(r'[\w\s]+', unformated_name)
    name =''.join(name) +'.jpg'
    img = request_page(link)
    
    with open(path+name, 'wb') as image_file:
        image_file.write(img.content)
        
        
def request_page(link):
    while True:
        try:
            req = requests.get(link)
            break
        except:
            print(f'failed to fetch data from {link}')
            print('tring again in 5 seconds')
            time.sleep(5)
            
    return req


def input_validation(start, end, msg=''):
    error_msg = f'Incorrect input, please provide a number between {start} and {end}'
    while True:
        value = input(msg)
        if value.isdigit():
            if int(value) < start or int(value) > end:
                print(error_msg)
            else:
                return value
        else:
            print(error_msg)
            
            
def input_validation_char(char_list,msg):
    options = '/'.join(char_list)
    error_msg = f'You can only choose from: [{options}]\n'
    while True:
        value = input(msg)
        if value.lower() in char_list:
            return value
        else:
            print('Sorry, incorrect input provided')
            print(error_msg)




genres = {1:'all', 2:'action', 3:'animation', 4:'comedy', 5:'drama', 6:'horror', 7:'sci-fi'}
languages = {1:'all', 2:'en', 3:'fr', 4:'it', 5:'ja', 6:'zh', 7:'ko', }
order = {1:'downloads', 2:'seeds', 3:'likes', 4:'rating', 5:'year', }
language_name = {'all':'All', 'en':'English', 'fr':'French', 'it':'Italian', 'ja':'Japanese',
                'zh':'Chinese', 'ko':'Korean', }

def print_info():

    
    print('''Details about the script.....
    Hello, this is a simple python script designed to scrap a movie site yts.mx
    In particular, it scraps movie details from the browse page of the site 

    for example the link of browse page conataining all genres, all languages and
    sorted by downloads is this 'https://yts.mx/browse-movies/0/all/all/0/downloads/0/all'

    things this script can scrap: movies's title, released year, rating, genre and movie cover

    you can select movies of particular genre and language
    and in the end you can specify how to sort the browse page

    this script creates a yts_scrap folder on your desktop and all the scrapped content is 
    saved there

    QUESTION: How long does this script take to execute?
        scraping a page without covers takes about 2 seconds
        scraping a page with covers takes about 30 seconds\n\n
    ''')


    print('*****OPTIONS*****')
    print('GENRES       ',end='')
    for index, name in genres.items():
        print(f'{index}: {name.title()}', end='  ')
    print('\n')

    print('LANGUAGES    ',end='')
    for index, name in languages.items():
        print(f'{index}: {language_name[name]}', end='  ')
    print('\n')

    print('ORDER BY     ',end='')
    for index, name in order.items():
        print(f'{index}: {name.title()}', end='  ')
    print('\n')


# printing welcome text
print_info()

# taking input from user
time.sleep(0.4)
genre_choice = int(input_validation(1,7,'Select Genre '))
language_choice = int(input_validation(1,7,'Select Language '))
order_choice = int(input_validation(1,5,'Order by '))
page_count = int(input_validation(1, 100, 'How many pages to scrap? [1-100] '))
scrap_covers = input_validation_char(['y','n'], 'Scrap movie covers too? [y/n] ')

# links to be scrapped
page1_link = f'https://yts.mx/browse-movies/0/all/{genres[genre_choice]}/0/{order[order_choice]}/0/{languages[language_choice]}'
next_link =  page1_link + '?page={}'

# showing selected options
print(f'''\nYou selected 
Genre: {genres[genre_choice].title()}
Language: {language_name[languages[language_choice]]}
Order by: {order[order_choice].title()}
\nFirst {page_count} page(s) of {page1_link} 
will be scrapped
''')

# estimated time logic
if scrap_covers[0].lower() == 'y':
    estimated_time = math.ceil((page_count*10)/60)
else:
    estimated_time = math.ceil((page_count*3)/60)
    
print(f'estimated time the script will take: {estimated_time} minutes\n')
input('Press enter key to continue ')



# creating directory on desktop of the user
username = os.getlogin()
os.mkdir(f'C:/Users/{username}/Desktop/yts_scrap')

if scrap_covers == 'y':
    os.mkdir(f'C:/Users/{username}/Desktop/yts_scrap/covers')

# opening a csv file
f = open(f'C:/Users/{username}/Desktop/yts_scrap/movies.csv', mode = 'w', newline='')
w = csv.writer(f, delimiter=',')

w.writerow(['name', 'year', 'rating', 'genres'])
start_time = time.perf_counter()
for n in range(1,page_count+1):
    print(f'Scraping page{n}', end=': ')
    
    if n == 1:
        req = request_page(page1_link)
    else:
        req = request_page(next_link.format(n))
            
        
    soup = bs4.BeautifulSoup(req.text, 'lxml')
    movies = soup.select('.browse-movie-wrap')
    
    if movies == []:
        print(f'\nEnd page{n} no further pages to scrap....')
        break

    for m in movies:
        movie_info = movie_details(m)
        w.writerow(movie_info)
        
    if scrap_covers == 'y':
        
        image_folder = f'C:/Users/{username}/Desktop/yts_scrap/covers/page{n}'
        os.mkdir(image_folder)
        
#         for m in movies:
#             save_cover(image_folder+'/', m)
          
        threads = []
        for m in movies:
            t = threading.Thread(target=save_cover, args=[image_folder+'/', m])
            t.start()
            threads.append(t)
    
        for t in threads:
            t.join()
        
    print('Completed')
    
f.close()  

script_time = time.perf_counter() - start_time
print('The script took {t:1.3} seconds'.format(t=script_time))
with open(f'C:/Users/{username}/Desktop/yts_scrap/scrape_info.txt', mode='w') as scrape_log:
    
    text = return_log(pages=page_count, link= page1_link,
          options=[genres[genre_choice].title(),language_name[languages[language_choice]],
          order[order_choice].title()], covers=scrap_covers)
    scrape_log.write(text)
    
print('Finished')