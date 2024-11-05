import json
from bs4 import BeautifulSoup

def save_techniques(data):
    soup = BeautifulSoup(data.content, 'html.parser')
    techniques_data = soup.find('tbody', class_='notion-collection-table__body')
    techniques = []
    for e in techniques_data:
        technique = {}
        technique['title'] = e.find('td', class_='title').text.strip()
        technique['tags'] = e.find('td', class_='multi_select').text.strip()
        technique['relation'] = e.find('td', class_='relation').text.strip()
        technique['status'] = e.find('td', class_='status').text.strip()

        techniques.append(technique)
    with open('techniques.json', 'w') as f:
        json.dump(techniques, f)
    return techniques
