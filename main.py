from fastapi import FastAPI, Request, HTTPException
import base64
import json
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "App runner is working 🎯"}

    
