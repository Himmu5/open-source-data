from bs4 import BeautifulSoup
import json

def save_actors(data):
    soup = BeautifulSoup(data.content, 'html.parser')
    actors_data = soup.find('tbody', class_='notion-collection-table__body')
    actors = []
    for e in actors_data:
        actor = {}
        actor['title'] = e.find('td', class_='title').text.strip()
        actor['Aliases'] = e.find('td', class_='text').text.strip()
        actor['Attribution'] = e.find('td', class_='select').text.strip()
        actor['Tags'] = e.find('td', class_='multi_select').text.strip()
        actor['Status'] = e.find('td', class_='status').text.strip()
        actor['targeted_geography'] = e.find('td', class_='status').text.strip()

        actors.append(actor)
    with open('actors.json', 'w') as f:
        json.dump(actors, f)
    return actors
        