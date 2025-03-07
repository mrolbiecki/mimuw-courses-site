import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import re
import time
import random
import json
import os

# URL of the website to scrape
url = "https://www.mimuw.edu.pl/pl/informator-dla-studentow/plany-studiow-czyli-co-kiedy-zaliczyc-i-podpiac/informatyka-i-stopnia/informatyka-i-stopien-rocznik-202223-202324/"

def get_courses_data():
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    table = soup.find('table', class_='study-programme')
    courses = []
    code_pattern = re.compile(r'\((\d{4}-[A-Za-z0-9]+)\)')  # Regex to match course codes like (1000-211cAM1)

    if table:
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 7:
                full_name = columns[0].text.strip()
                lecture_hours = columns[1].text.strip()
                practical_hours = columns[2].text.strip()
                lab_hours = columns[3].text.strip()
                total_hours = columns[4].text.strip()
                ects = columns[5].text.strip()
                form_of_credit = columns[6].text.strip()

                # Extract course code using regex
                match = code_pattern.search(full_name)
                course_code = match.group(1) if match else ''
                course_name = re.sub(code_pattern, '', full_name).strip()  # Remove code from name

                if course_code:
                    courses.append({
                        'course_name': course_name,
                        'course_code': course_code,
                        'lecture_hours': lecture_hours,
                        'practical_hours': practical_hours,
                        'lab_hours': lab_hours,
                        'total_hours': total_hours,
                        'ects': ects,
                        'form_of_credit': form_of_credit
                    })
    return courses


CACHE_FILE = "search_cache.json"

def get_books(course_name):

    # Load cache if it exists
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as cache_file:
            search_cache = json.load(cache_file)
    else:
        search_cache = {}

    search_query = course_name + " site:https://ksiegarnia.pwn.pl/"
    if search_query in search_cache:
        books = search_cache[search_query]
    else:
        books = list(DDGS().text(search_query, max_results=5))
        search_cache[search_query] = books

        # Save cache to disk
        with open(CACHE_FILE, "w") as cache_file:
            json.dump(search_cache, cache_file)

        # Add a random delay to avoid being flagged
        time.sleep(random.uniform(2, 5))

    return books