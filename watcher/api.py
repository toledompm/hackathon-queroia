from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from utils.oci_bucket import create_oci_bucket

load_dotenv()

app = FastAPI()

bucket = create_oci_bucket()

@app.get("/")
async def search():
    return {"message": "Hello World"}


@app.post("/")
async def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        bucket.upload_file(file.filename, contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}
