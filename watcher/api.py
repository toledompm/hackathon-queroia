import os
from threading import Event, Thread
import time
from numpy import array
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from utils.oci_bucket import create_oci_bucket
from database.in_memory import InMemoryDB
from handlers.indexer import Indexer
from utils.watcher import watch
from model.embedding_model import EmbeddingModel

load_dotenv()


reconciliation_interval = float(os.environ["RECONCILIATION_INTERVAL_MINUTES"]) * 60

bucket = create_oci_bucket()
embeddingModdel = EmbeddingModel()
db = InMemoryDB(os.environ["DB_FILE"])
indexer = Indexer(os.environ["INDEX_FILE"], db, embeddingModdel)


app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def search(query: str = ""):
    if query == "":
        return {"message": "No query provided"}

    data = db.get()
    embeddings = data.embedding.apply(array)
    indexes = embeddingModdel.search(query, embeddings)
    res = data.iloc[indexes].to_dict("records")

    return {"results": res}


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


def watch_loop(event: Event):
    while True:
        if event.is_set():
            return
        watch(bucket, indexer)
        time.sleep(reconciliation_interval)


watch_thread_stop_event = Event()
watch_thread = Thread(target=watch_loop, args=(watch_thread_stop_event,))
watch_thread.start()


@app.on_event("shutdown")
def shutdown_event():
    watch_thread_stop_event.set()
