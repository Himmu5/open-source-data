import boto3
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
