import sys

sys.path.insert(0, r"D:\deeksha_repo\fast-api-app-\backend")
sys.path.insert(0, r"D:\deeksha_repo\fast-api-app-\backend\.runtime-pkgs")

import uvicorn

uvicorn.run("app.main:app", host="127.0.0.1", port=8000)
