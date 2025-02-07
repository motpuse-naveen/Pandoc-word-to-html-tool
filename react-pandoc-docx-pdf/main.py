import os
import subprocess
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure 'uploads' folder exists
os.makedirs("uploads", exist_ok=True)

# Mount uploads folder to serve files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.post("/convert-docx-to-html/")
async def convert_docx_to_html(file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"
    html_output = f"uploads/{file.filename}.html"

    # Save the uploaded DOCX file
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Convert DOCX to HTML using Pandoc
    pandoc_command = f"pandoc {file_location} -o {html_output} --self-contained"

    try:
        result = subprocess.run(pandoc_command, check=True, shell=True, capture_output=True, text=True)
        print("Pandoc Output:", result.stdout)
        print("Pandoc Errors:", result.stderr)

        if os.path.exists(html_output):
            print(f"✅ HTML file created: {html_output}")
            return {"html_file": f"http://localhost:8000/uploads/{file.filename}.html"}
        else:
            print(f"❌ Pandoc did not generate the file: {html_output}")
            return {"error": "Pandoc conversion failed."}

    except subprocess.CalledProcessError as e:
        print("❌ Pandoc Error:", e.stderr)
        return {"error": f"Pandoc failed: {e.stderr}"}
