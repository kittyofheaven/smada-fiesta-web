import uvicorn
from fastapi import FastAPI, BackgroundTasks
from send_email import send_email_background, send_email_async

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)