import requests
from fastapi import FastAPI
from bs4 import BeautifulSoup
import json
from s3_session import upload_json_to_s3

app = FastAPI()

@app.get("/")
async def read_root():
    data = get_raw_data('all-incidents')
    actorhtml = get_raw_data("all-actors")
    techniques_html = get_raw_data('all-techniques')
    threats = save_incidents(data)
    actors = save_actors(actorhtml)
    techniques = save_techniques(techniques_html)

    await upload_json_to_s3(techniques, 'techniques.json')
    await upload_json_to_s3(actors, 'actors.json')
    await upload_json_to_s3(threats, 'incidents.json')
    final_data = {'threats': threats, 'actors': actors, 'techniques': techniques}
    return final_data

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

def get_raw_data(url: str):
    response = requests.get("https://threats.wiz.io/"+url)
    return response
