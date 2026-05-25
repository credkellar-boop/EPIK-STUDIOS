import os
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from brain.engine import compile_epic_studio_macro

app = FastAPI(title="EPIC-STUDIO'S API Platform")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "result": None, 
            "export_status": None, 
            "initial_val": "Create a piano roll macro that humanizes performance velocities."
        }
    )

@app.post("/compile")
async def compile_script(request: Request, prompt: str = Form(...)):
    if not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt layer empty.")
    
    try:
        # Calls Module 1 orchestration layer clean
        compiled_code = compile_epic_studio_macro(prompt)
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request, 
                "result": compiled_code, 
                "export_status": "Success",
                "initial_val": prompt
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request, 
                "result": f"[ERROR]: {str(e)}", 
                "export_status": "Export failed due to engine runtime error.",
                "initial_val": prompt
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
