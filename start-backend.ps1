Set-Location "$PSScriptRoot\backend"
& "$PSScriptRoot\backend\env\Scripts\python.exe" -m uvicorn app.main:app --reload
