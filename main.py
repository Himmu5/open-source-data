import requests
from fastapi import FastAPI
from s3_session import upload_json_to_s3
from techniques import save_techniques
from actor import save_actors
from incidents import save_incidents
from s3_session import get_file_from_s3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get('/open-source')
async def get_data(dataType: str):
    if dataType == None:
        return {'error': 'Please provide a data type'}
    elif dataType == 'techniques':
        data= await get_file_from_s3('techniques.json')
        return { "data": data, "message": "Data fetched successfully", "status": 200}
    elif dataType == 'actors':
        data= await get_file_from_s3('actors.json')
        return { "data": data, "message": "Data fetched successfully", "status": 200}
    elif dataType == 'incidents':
        data= await get_file_from_s3('incidents.json')
        return { "data": data, "message": "Data fetched successfully", "status": 200}
    else:
        return {'error': 'Invalid data type'}

def get_raw_data(url: str):
    response = requests.get("https://threats.wiz.io/"+url)
    return response
