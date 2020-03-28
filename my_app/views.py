import requests
import urllib
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from .models import Search
import re


BASE_CRAIGLIST_URL ="https://sfbay.craigslist.org/search/?query={}"
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'



''' Render Home Page'''
def home(request):
    return render (request, template_name='base.html')


''' Search Function'''
def new_search(request):
    #Get data from search box
    search = request.POST.get('search')
    
    #Interacting With db to save searvh data(populating data)
    Search.objects.create(search=search)

    
    '''Webscrapping Engine'''
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    # Getting the webpage.

    response = uReq(final_url)
    # Extracting the webpage HTML codes.
    data = response.read()
    # Creating a Beautiful Soup Object.
    soup =  BeautifulSoup(data, 'html.parser')
    # closing connection
    response.close()
    # Extracting all the <li> tag whose class is 'result-row' into a list.
    search_listings = soup.find_all('li', {'class': 'result-row'})
    
    final_postings= []

    # To acess each List.
    for ad in search_listings:
        post_title = ad.find(class_='result-title').text #Extracting the Title of the Ad.
        post_url = ad.find('a').get('href') #Extracting the Link to Ad Exact Page.

        '''Checking if the Price can be extracted in the Search Page'''

        if ad.find(class_='result-price'):
            post_price = ad.find(class_='result-price').text #Extracting the Price in an Ad.
        else:
            post_price= 'N/A'
            #Webcraping the from the Ad Url
            ''' new_response = requests.get(post_url)
            new_data = new_response.text
            new_soup =  BeautifulSoup(new_data, 'html.parser')
            post_text = new_soup.find(id='postingbody').text

            r1 = re.findall(r'\$\w+', post_text)
            if r1:
                post_price =r1[0]
            else:
                post_price = 'N/A' '''

        if ad.find(class_='result-image').get('data-ids'):
            post_image_id = ad.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://cdn.pixabay.com/photo/2018/02/14/12/44/business-cards-3152885_960_720.jpg'


        final_postings.append((post_title, post_url, post_price, post_image_url))
    
    

    content={
        "search": search, 
        "final_postings": final_postings,
    }
    return render (request, template_name='my_app/new_search.html', context = content)