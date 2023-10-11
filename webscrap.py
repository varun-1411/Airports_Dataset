import requests
from bs4 import BeautifulSoup

# Making a GET request
r = requests.get('https://www.newdelhiairport.in/delseworldtak')

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

s = soup.find('div', class_='entry-content')
content = s.find_all('p')

import h5py

file = "Disruptions_Q1_2015_def.h5"
h5 = h5py.File(file, 'r')

datasetNames = [n for n in h5.keys()]
for n in datasetNames:
    print(n)