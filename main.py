import requests
from fastapi import FastAPI
from s3_session import upload_json_to_s3
from techniques import save_techniques
from actor import save_actors
from incidents import save_incidents

app = FastAPI()

@app.get("/wiz/scrapper")
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

def get_raw_data(url: str):
    response = requests.get("https://threats.wiz.io/"+url)
    return response
