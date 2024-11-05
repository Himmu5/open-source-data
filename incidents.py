from bs4 import BeautifulSoup
import json

def save_incidents(data):
    soup = BeautifulSoup(data.content, 'html.parser')
    incedents=soup.find_all('tbody', class_='notion-collection-table__body')
    threats = []
    for e in incedents[0]:
        threat = {}
        threat['title'] = e.find('td', class_='title').text.strip()
        threat['actor'] = e.find('td', class_='relation').text.strip()
        threat['status'] = e.find('td', class_='status').text.strip()
        threat['date'] = e.find('td', class_='date').text.strip() 
        threat['type'] = e.find('td', class_='select').text.strip()
        threat['initial_access'] = e.find('td', class_='notion-collection-table__cell multi_select').text.strip()

        threats.append(threat)
    with open('incidents.json', 'w') as f:
        json.dump(threats, f)
    return threats