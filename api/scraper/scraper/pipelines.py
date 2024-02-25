# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from bs4 import BeautifulSoup
from itemadapter import ItemAdapter
import subprocess
from reports.models import Country
from asgiref.sync import sync_to_async
from scrapy.exceptions import DropItem

class ScraperPipeline(object):
    """
    Saves Item to the database using sync_to_async
    """

    @sync_to_async
    def save_to_database(self, item, spider):
        # Your database-saving logic here
        # Replace the following lines with your actual database-saving code
        item_data = dict(item)

        if spider.name == "cdc":
            try:
                # Try to get the existing record
                country, created = Country.objects.get_or_create(name=item_data.get('name'))

                if not created:
                    # Update specific fields while preserving others
                    update_fields = ['diseases', 'health_report', 'vaccines']
                    for field in update_fields:
                        setattr(country, field, item_data.get(field, getattr(country, field)))
                    country.save()
            except Exception as e:
                print(f"Failed to save to the database: {e}")
        else:
            try:
                # Create a new record
                Country.objects.create(**item_data)
            except Exception as e:
                print(f"Failed to save to the database: {e}")


    async def process_item(self, item, spider):
        # Convert Scrapy item to a dictionary

        # Use sync_to_async to save to the database
        await self.save_to_database(item, spider)

        return item



class TravelAdvisoryPipeline(object):
    def process_item(self, item, spider):
        if item.get('travel_safety_report') and spider.name == "state":
            soup = BeautifulSoup(item.get('travel_safety_report'), 'html.parser')
            for li_tag in soup.find_all('li'):
                if 'Smart Traveler Enrollment Program' in li_tag.get_text() or 'Follow the Department of State on' in li_tag.get_text() or 'Visit the CDC page for the latest' in li_tag.get_text():
                    li_tag.decompose()
            # Replace links with their plaintext
            for a_tag in soup.find_all('a'):
                a_tag.replace_with(f"{a_tag.get('href')} ({a_tag.text})")

            plaintext = soup.get_text(separator=' ', strip=True)
            item['travel_safety_report'] = plaintext

        if item.get('name') and spider.name == "state":
            country_name = ""
            name = item.get('name')
            if isinstance(name, list):
                # If it's a list, take the first element
                name = str(name[0]) if name else ""
            else:
                # If it's not a list, just convert to string
                name = str(name)
            
            url_list = name.split('/')[-1].split('-')
            list_of_country = []
            
            for word in url_list:
                list_of_country.append(word)

            # Check for the presence of "travel" in the entire URL
            if "travel" in name.lower():
                country_name = " ".join(list_of_country).title()

            def return_country(string):
                ret = []
                for name in string.split(" "):
                    if name=="Travel":
                        return ' '.join(ret)
                    ret.append(name)

            item['name'] = return_country(country_name)

        return item


class HealthAdvisoryPipeline(object):
    def process_item(self, item, spider):
        #Extract Diseases
        if spider.name == "cdc":
            if item.get('diseases'):
                text_list = [BeautifulSoup(str(html), 'html.parser').get_text() for html in item.get('diseases')]
                item['diseases'] = ', '.join(text_list)
            if item.get('health_report'):
                text = BeautifulSoup(str(item.get('health_report')), 'html.parser').get_text()
                item['health_report'] = text
            if item.get('vaccines'):
                text_list = [BeautifulSoup(str(html), 'html.parser').get_text() for html in item.get('vaccines')]       
                item['vaccines'] = ', '.join(text_list)
            if item.get('name'):
                url_split = ((item.get('name')[0].split('/'))[-1]).split('-')
                url_split = ' '.join(url_split).title()
                item['name'] = url_split
        return item

