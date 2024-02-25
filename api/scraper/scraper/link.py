import subprocess
import json
import re
import subprocess
from bs4 import BeautifulSoup
import requests
import sys

from reports.models import Country

class LinkFinder():
    def return_state_urls(self):
        proc = subprocess.Popen(["curl", "https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories/north-macedonia-travel-advisory.html"], stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        pattern = re.compile(r'var availableTags = (\[.*?\]);', re.DOTALL)
        curl_data = pattern.search(str(out)).group(1)

        urls = [url.strip() for url in curl_data.split('\\n')]

        urls = [url for url in urls if len(url)>6]

        urls = [''.join(["https://travel.state.gov", url.split(",")[1][6:].replace('"', ""), ".html"]) for url in urls]
        
        return urls

    def return_cdc_urls(self):
        def is_valid_url(url):
            try:
                response = requests.head(url)
                return response.status_code == 200
            except requests.RequestException:
                return False
            
        proc = subprocess.Popen(["curl", "https://wwwnc.cdc.gov/travel/destinations/list"], stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        soup = BeautifulSoup(str(out), 'html.parser')
        
        # Find all <a> tags with href attribute
        all_links = soup.find_all('a', href=True)
        relevant_links = []
        for link in all_links:
            if link['href'] is not None and link['href'].startswith('/travel/destinations/traveler'):
                relevant_links.append(''.join(["https://wwwnc.cdc.gov", link['href']]))
        
        names_list = Country.objects.values_list('name', flat=True)
        filtered_urls = []
        for name in names_list:
            name = name.split(' ')
            name = '-'.join(name)
            url = f'https://wwwnc.cdc.gov/travel/destinations/traveler/none/{name.lower()}'
            filtered_urls.append(url)
        valid_urls = [url for url in filtered_urls if is_valid_url(url)]
        return valid_urls
