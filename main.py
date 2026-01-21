from fastapi import FastAPI, Request, HTTPException
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "App runner is working 🎯"}

def get_groups(request: Request):
    claims = request.scope["aws.event"]["requestContext"]["authorizer"]["jwt"]["claims"]
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
    
