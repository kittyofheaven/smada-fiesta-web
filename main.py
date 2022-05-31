import uvicorn
from fastapi import FastAPI, BackgroundTasks
from send_email import send_email_background
from pydantic import BaseModel, EmailStr
from typing import List


app = FastAPI()

# print(Envs.MAIL_USERNAME)

@app.get('/')
def index():
    return 'Hello World'


# EMAIL SECTION

class EmailSchema(BaseModel):
    email: List[EmailStr]

# @app.get('/send-email/asynchronous')
# async def send_email_asynchronous():
#     await send_email_async('Hello World','hazelhandrata@gmail.com',
#     "halo")
#     return 'Success'

@app.post('/send-email') # ini send email background
def send_email_backgroundtasks(background_tasks: BackgroundTasks, email: EmailSchema):
    send_email_background(background_tasks, 'Hello World',  # disini title 
    email.dict().get("email"), 'halo') # disini body

    # print(email.dict().get("email"))
    return 'Success'

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)