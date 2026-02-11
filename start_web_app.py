import uvicorn
import os
import sys

# Add src to python path just in case
sys.path.insert(0, os.getcwd())

if __name__ == "__main__":
    print("Starting Rad-LOINC Web Interface...")
    print("Open http://localhost:8000 in your browser")
    uvicorn.run("src.web_api:app", host="0.0.0.0", port=8000, reload=True)
