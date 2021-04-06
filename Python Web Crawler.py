import json
import requests
from bs4 import BeautifulSoup
import re

# Python web scrapper that fetches info of wanted suspects on given website and outputs all info as json file
# Author: Justin Scott
# Date: 4-5-21

# Writing out given constants
source_code = 'EU_MWL'
source_name = 'Europe Most Wanted List'
source_url = 'https://eumostwanted.eu/'

# Getting page info using BeautifulSoup and parsing the html to use later
page = requests.get(source_url)
soup = BeautifulSoup(page.content, 'html.parser')

# Filtering results from request above to just the content in the html div class 'div-content'
results = soup.findAll('span', {'class': 'field-content'})

# Even further filtering results by grabbing the tags with urls that match the regex logic
# for all 3 url types I found on given website and combining them
filtered_results_url1 = re.findall('https:\/\/eumostwanted.eu\/\w+-\w+', ''.join([str(x) for x in results]))
filtered_results_url2 = re.findall('https:\/\/eumostwanted.eu\/\w+-\w+-\w+', ''.join([str(x) for x in results]))
filtered_results_url3 = re.findall('https:\/\/eumostwanted.eu/node/[0-9]{4}', ''.join([str(x) for x in results]))
total_results = filtered_results_url1 + filtered_results_url2 + filtered_results_url3

# Creating dictionary to setup json file output
data = {
    'source_code': source_code,
    'source_name': source_name,
    'source_url': source_url,
    'people': []
}

# Iterate through filtered results to find specific info of each suspect
for i in total_results:
    response = requests.get(i)
    # Check to see if page still exists
    if response.status_code == 200:
        response_soup = BeautifulSoup(response.content, 'html.parser')
        details = response_soup.find('div', {'class': 'wanted_top_right'})

        # Fetch specific info of suspect
        name = details.find('div', {'class': 'field field-name-title-field field-type-text field-label-hidden field-wrapper'})
        date_of_birth = details.find('div', {'class': 'field field-name-field-date-of-birth field-type-datetime field-label-inline clearfix clearfix field-wrapper'})
        crime = details.find('div', {'class': 'field field-name-field-crime field-type-taxonomy-term-reference field-label-inline clearfix clearfix field-wrapper'})
        sex = details.find('div', {'class': 'field field-name-field-gender field-type-taxonomy-term-reference field-label-inline clearfix clearfix field-wrapper'})
        eye_color = details.find('div', {'class': 'field field-name-field-eye-colour field-type-taxonomy-term-reference field-label-inline clearfix clearfix field-wrapper'})
        nationality = details.find('div', {'class': 'field field-name-field-nationality field-type-taxonomy-term-reference field-label-inline clearfix clearfix field-wrapper'})
        ethnic_origin = details.find('div', {'class': 'field field-name-field-ethnic-origin field-type-taxonomy-term-reference field-label-inline clearfix clearfix field-wrapper'})
        spoken_languages = details.find('div', {'class': 'field field-name-field-languages field-type-taxonomy-term-reference field-label-inline clearfix clearfix field-wrapper'})
        state_of_case = details.find('div', {'class': 'field field-name-field-state-of-case field-type-taxonomy-term-reference field-label-inline clearfix clearfix field-wrapper'})

        # Set fetched info of suspect to text, if None, text is NA to prevent errors
        name = name.text if name is not None else 'NA'
        date_of_birth = date_of_birth.text if date_of_birth is not None else 'NA'
        crime = crime.text if crime is not None else 'NA'
        sex = sex.text if sex is not None else 'NA'
        eye_color = eye_color.text if eye_color is not None else 'NA'
        nationality = nationality.text if nationality is not None else 'NA'
        ethnic_origin = ethnic_origin.text if ethnic_origin is not None else 'NA'
        spoken_languages = spoken_languages.text if spoken_languages is not None else 'NA'
        state_of_case = state_of_case.text if state_of_case is not None else 'NA'

        # Add info to json file
        data['people'].append({
            'name': name,
            'date_of_birth': date_of_birth,
            'crime': crime,
            'sex': sex,
            'eye_color': eye_color,
            'nationality': nationality,
            'ethnic_origin': ethnic_origin,
            'spoken_languages': spoken_languages,
            'state_of_case': state_of_case
        })

# Output json file
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
