from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
import subprocess
from jinja2 import Environment, FileSystemLoader

app = FastAPI()

app.mount("/static", StaticFiles(directory="web/static"), name="static")
BASE_ARTICLES_DIR = Path("articles")
templates = Environment(loader=FileSystemLoader("web/templates"))

@app.get("/", response_class=HTMLResponse)
async def home():
    template = templates.get_template("home.html")
    recent_topics = [folder.name for folder in BASE_ARTICLES_DIR.iterdir() if folder.is_dir()]
    return HTMLResponse(content=template.render(recent_topics=recent_topics))

@app.post("/generate")
async def generate_article(topic: str = Form(...)):
    output_path = BASE_ARTICLES_DIR / topic.replace(" ", "_")
    os.makedirs(output_path, exist_ok=True)
    subprocess.run(["python3", "main.py"], input=topic.encode())
    return JSONResponse(content={"redirect": f"/results/{topic.replace(' ', '_')}/"})

# Route to show available results for a topic (lists timestamp subdirectories)
@app.get("/results/{topic}", response_class=HTMLResponse)
async def show_topic_results(topic: str):
    formatted_topic = topic.replace(" ", "_")
    topic_path = BASE_ARTICLES_DIR / formatted_topic
    if not topic_path.exists():
        return HTMLResponse(content=f"No results found for {formatted_topic}.", status_code=404)
    # List all subdirectories (timestamps) for the topic, sorted in reverse order (latest first)
    subdirs = sorted([folder.name for folder in topic_path.iterdir() if folder.is_dir()], reverse=True)
    template = templates.get_template("topic_results.html")
    return HTMLResponse(content=template.render(topic=formatted_topic, subdirs=subdirs))

# Route to show files for a specific timestamp result
@app.get("/results/{topic}/{timestamp}", response_class=HTMLResponse)
async def show_timestamp_results(topic: str, timestamp: str):
    formatted_topic = topic.replace(" ", "_")
    result_path = BASE_ARTICLES_DIR / formatted_topic / timestamp
    if not result_path.exists():
        return HTMLResponse(content=f"No results found for {formatted_topic} at {timestamp}.", status_code=404)
    files = [file.name for file in result_path.iterdir() if file.suffix == ".txt"]
    template = templates.get_template("results.html")
    return HTMLResponse(content=template.render(topic=formatted_topic, timestamp=timestamp, files=files))

# Download route including timestamp
@app.get("/download/{topic}/{timestamp}/{filename}")
async def download_file(topic: str, timestamp: str, filename: str):
    file_path = BASE_ARTICLES_DIR / topic / timestamp / filename
    if file_path.exists():
        return FileResponse(file_path, filename=filename)
    return JSONResponse(content={"error": "File not found"}, status_code=404)


# Run the ASGI app directly when invoked with python web/app.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)