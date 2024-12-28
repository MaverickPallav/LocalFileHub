from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import os
import time
from pydantic import BaseModel

app = FastAPI()

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

class UploadRequest(BaseModel):
    filePath: str
    overwrite: bool = False

@app.post("/upload")
async def upload_file(request: UploadRequest):
    try:
        file_name = os.path.basename(request.filePath)

        if not os.path.exists(request.filePath):
            raise HTTPException(status_code=404, detail="File not found at the specified path")

        if request.overwrite:
            destination_filename = file_name
        else:
            milliseconds_since_epoch = int(time.time() * 1000)
            file_base, file_ext = os.path.splitext(file_name)
            destination_filename = f"{file_base}_{milliseconds_since_epoch}{file_ext}"

        destination_path = os.path.join(UPLOAD_FOLDER, destination_filename)

        with open(request.filePath, "rb") as src_file:
            with open(destination_path, "wb") as dest_file:
                dest_file.write(src_file.read())

        download_link = f"http://localhost:8000/download/{destination_filename}"
        return JSONResponse({"download_link": download_link})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)