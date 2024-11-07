import boto3
import json
from fastapi import UploadFile, HTTPException

def create_client():
    return boto3.client('s3', region_name="us-east-1")



async def upload_json_to_s3(file, fileName):
    s3_client=create_client()
    try:
        
        # Set the bucket name and the file name (key) in S3
        bucket_name = "threat-data-wiz"
        key = f"{fileName}"

        # Upload to S3
        with open(f"{fileName}", 'rb') as file:
            s3_client.upload_fileobj(
                file,
                bucket_name,
                fileName
            )

        return {"message": f"File uploaded successfully to {bucket_name}/{key}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

async def get_file_from_s3(file_name):
    s3 = boto3.resource('s3')
    try:
        obj = s3.Object('threat-data-wiz', file_name)
        data=obj.get()['Body'].read()
        return json.loads(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")