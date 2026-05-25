import os
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from brain.engine import run_epic_engine

app = FastAPI(title="EPIC-STUDIO'S API Platform")

# Setup template engine directory
templates = Jinja2Templates(directory="templates")

class ScriptRequest(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    """Serves the main web administration front panel."""
    return templates.TemplateResponse("index.html", {"request": request, "result": None, "initial_val": "Create a piano roll script that automates velocity dynamics and applies an auto-tone key filter."})

@app.post("/compile")
async def compile_script(request: Request, prompt: str = Form(...)):
    """
    Asynchronous Backend endpoint that connects the frontend action 
    directly to the GitHub Scraper and Gemini AI Engine.
    """
    if not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt layer cannot be empty.")
    
    try:
        # Run calculation via our background processing engine
        compiled_code = run_epic_engine(prompt)
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "result": compiled_code, 
            "initial_val": prompt
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "result": f"[ERROR BRIDGE CRITICAL]: {str(e)}", 
            "initial_val": prompt
        })

if __name__ == "__main__":
    import uvicorn
    # Start server on local development port 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
