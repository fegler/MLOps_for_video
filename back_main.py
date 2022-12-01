from fastapi import UploadFile, File, FastAPI, Header
from typing import List, Union

import os
import numpy as np
import datetime
from fastapi.responses import FileResponse, HTMLResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static/")
IMG_DIR = os.path.join(BASE_DIR, "data/")

if not os.path.isdir(STATIC_DIR):
    os.mkdir(STATIC_DIR)
if not os.path.isdir(IMG_DIR):
    os.mkdir(IMG_DIR)

router = FastAPI()
CHUNK_SIZE = 1024 * 1024
file_names = []


@router.post("/uploadfiles")
async def upload_file(files: List[UploadFile] = File(...)):
    file_urls = []
    for file in files:
        saved_file_name = "tmp.jpg"
        file_location = os.path.join(IMG_DIR, saved_file_name)
        file_urls.append(file_location)
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
    result = {"fileUrls": file_urls}
    return result


@router.get("/images/{file_name}")
def get_image(file_name: str):
    return FileResponse(os.path.join(IMG_DIR, file_name))


@router.get("/")
async def main():
    content = """
    <body>
    <form action="/uploadfiles" enctype="multipart/form-data" method="post">
    <input name="files" type="file" accept="image/*" multiple>
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)
