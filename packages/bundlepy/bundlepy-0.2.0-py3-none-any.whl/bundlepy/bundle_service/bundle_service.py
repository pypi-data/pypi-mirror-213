import base64
import multiprocessing
import os
import subprocess
import tempfile
import shutil
import sys
import zipfile

from contextlib import contextmanager

import uvicorn

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from bundlepy.bundler import Bundler

app = FastAPI()

class CompileTask(BaseModel):
    packages: list
    transitive_imports: list
    entry_point: str
    project_file: str
    project_name: str

def _bundle(entry_point, packages, transitive_imports, proj_dir):
    bundler = Bundler(os.path.join(proj_dir, entry_point),
                        packages, transitive_imports)
    bundler.bundle_app()

def _prepare_project_space(filename: str, file_data, proj_dir):
    with open(os.path.join(proj_dir, filename), "wb") as uploaded_file:
        uploaded_file.write(file_data)
    with zipfile.ZipFile(os.path.join(proj_dir, filename), 'r') as zip_ref:
        zip_ref.extractall(proj_dir)

def _get_base64(file_path: str):
    with open(file_path, "rb") as exe:
        return base64.b64encode(exe.read()).decode("utf-8")

# @app.post("/uploadfile")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    with open(file.filename, "wb") as uploaded_file:
        uploaded_file.write(contents)
    return {"filename": file.filename}

@app.post("/bundle")
async def compile(project_info: CompileTask):
    zip_data = base64.b64decode(project_info.project_file)
    tmp_dir = tempfile.mkdtemp()
    _prepare_project_space(project_info.project_name, zip_data, tmp_dir) 
    prev_dir = os.getcwd()
    os.chdir(tmp_dir)
    bundler_proc = multiprocessing.Process(target=_bundle,
                                            args=(os.path.join(tmp_dir, project_info.entry_point),
                                                  project_info.packages, project_info.transitive_imports, tmp_dir,))
    bundler_proc.start()
    bundler_proc.join()
    if os.name == "posix":
        exe_name = os.path.splitext(project_info.entry_point)[0]
    else:
        exe_name = os.path.splitext(project_info.entry_point)[0] + ".exe"
    compiled_binary_path = os.path.join("dist",
                                        exe_name)
    
    encoded_exe = _get_base64(compiled_binary_path)
    os.chdir(prev_dir)
    shutil.rmtree(tmp_dir)
    return {"file": encoded_exe}

def main():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    port_number = 8080 if os.name == "posix" else 80
    uvicorn.run("bundle_service:app", host=os.environ.get("BUNDLEPY_HOST_IP", "0.0.0.0"),
                port=int(os.environ.get("BUNDLEPY_PORT", port_number)), reload=os.environ.get("BUNDLEPY_DEBUG", False),
                workers=os.environ.get("BUNDLE_PY_WORKER_COUNT", 2),
                timeout_keep_alive=300)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
