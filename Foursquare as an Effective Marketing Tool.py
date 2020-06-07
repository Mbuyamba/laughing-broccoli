#!/usr/bin/env python
# coding: utf-8

# In[6]:



import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

get_ipython().system('conda install -c conda-forge geopy --yes ')
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')
import folium # plotting library

print('Folium installed')
print('Libraries imported.')


# In[7]:


CLIENT_ID = 'KKJXGJCS3TYFUN1Z54TQZT0CLQRBZ3IBFMF1TOSBHZHBLAOF' # my Foursquare ID
CLIENT_SECRET = 'YO3S5CZPLOFDW0AC2PO1YFD0KVRXJMP0W24RPLB11KSJ0EWS' # my Foursquare Secret ID
VERSION = '20200607' # Today's date
LIMIT = 10000
print('My credentails:')
print('CLIENT_ID:' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# In[8]:


address = '13620 97 St NW, Edmonton, AB'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)


# In[9]:


search_query = 'Restaurants'
radius = 217723962
url = 'https://api.foursquare.com/v2/venues/search?client_id=KKJXGJCS3TYFUN1Z54TQZT0CLQRBZ3IBFMF1TOSBHZHBLAOF&client_secret=YO3S5CZPLOFDW0AC2PO1YFD0KVRXJMP0W24RPLB11KSJ0EWS&ll=53.59886,-113.4923479&v=20200607&query=Restaurants&radius=217723962&limit=10000'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
url


# In[11]:


results = requests.get(url) .json()
results


# In[30]:


get_ipython().system('pip install flatten_json')


# In[33]:


import pandas
from pandas.io.json import json_normalize
pandas.json_normalize(results)
print(results)


# In[34]:


venues = results['response']['venues']
dataframe = json_normalize(venues)
dataframe.head()


# In[41]:


# keep only columns that include venue name, and anything that is associated with location

filtered_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')] + ['id']
dataframe_filtered = dataframe.loc[:, filtered_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
dataframe_filtered['categories'] = dataframe_filtered.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered.columns = [column.split('.')[-1] for column in dataframe_filtered.columns]

dataframe_filtered.head()


# In[45]:


dataframe_filtered.drop(['labeledLatLngs', 'crossStreet', 'country', 'state', 'city', 'cc', 'postalCode', 'address', 'neighborhood'], axis=1, inplace=True)
dataframe_filtered.head()


# In[46]:


venue_id = '50be79e7067d9b23974f32db' # Nearest Joey's Seafood Restaurants id
url = 'https://api.foursquare.com/v2/venues/50be79e7067d9b23974f32db?client_id=KKJXGJCS3TYFUN1Z54TQZT0CLQRBZ3IBFMF1TOSBHZHBLAOF&client_secret=YO3S5CZPLOFDW0AC2PO1YFD0KVRXJMP0W24RPLB11KSJ0EWS&v=20200607'.format(venue_id, CLIENT_ID, CLIENT_SECRET, VERSION)
url


# In[47]:


# Exploring a restaurant in the city to have a better idea of its needs
result = requests.get(url).json()
print(result['response']['venue'].keys())
result['response']['venue']


# In[65]:


# Restaurant Rating - 

try:
    print(result['response']['venue']['rating'])
except:
    print('Rating not available.')


# In[66]:


result['response']['venue']['tips']['count']


# In[ ]:




