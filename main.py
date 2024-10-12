# user-management-service/main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/user-management")
async def user_management_root():
    return {"message": "User Management Blue Green"}

@app.get("/user-management/health")
async def health():
    return {"status": "OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)