from fastapi import FastAPI, Request, HTTPException
import base64
import json
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "App runner is working 🎯"}

def get_groups(request: Request):
    oidc_data = request.headers.get("x-amzn-oidc-data")
    if not oidc_data:
        raise HTTPException(status_code=401, detail="Missing token data")

    payload = oidc_data.split(".")[1]
    payload += "=" * (-len(payload) % 4)  # pad base64
    claims = json.loads(base64.b64decode(payload))

    return claims.get("cognito:groups", [])

@app.get("/admin")
def admin(groups=get_groups):
    if "admin" not in groups:
        raise HTTPException(status_code=403, detail="Admin only")
    return {"message": "Admin access success"}

@app.get("/ground")
def ground(groups=get_groups):
    if not set(groups) & {"admin", "ground_station_user"}:
        raise HTTPException(status_code=403)
    return {"message": "Ground station access success"}

@app.get("/satellite")
def satellite():
    return {"message": "Satellite access success"}
    
# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=8080,
#         log_level="info"
#     )
    
