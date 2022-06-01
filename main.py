import uvicorn
import random
import re
from fastapi import FastAPI, BackgroundTasks
from send_email import send_email_background, send_email_async
from pydantic import BaseModel, EmailStr
from typing import List
from link_generator import link_generator, used_number_delete

from database import bandcomp_vote, searh_bandcomp_otp, bandcomp_vote_verificated

### TODO LIST ###
# buat link yg dikirim ke pengguna itu jadi dalam bentuk yang pasti
# html buat email
# integrasi html email ke app fastapi
# mekanisme voting

app = FastAPI()

# print(Envs.MAIL_USERNAME)

@app.get('/')
def index():
    return 'Hello World'


# EMAIL SECTION

class BandcompSchema(BaseModel):
    email: EmailStr
    who: str

# @app.post('/send-email/asynchronous')
# async def send_email_asynchronous(email: EmailSchema):
#     link_exten = link_generator(email.dict().get("email")[0])
#     await send_email_async('Hello World',email.dict().get("email"),
#     link_exten)
#     return 'Success'

# def link_generator(email):
#     email = email.lower()
    
#     rand_num = random.randint(1000000, 9999999)

# verif_list = [] # list email yg belum verifikasi

@app.post('/bandcomp/send-email') # ini send email background
def send_email_backgroundtasks(background_tasks: BackgroundTasks, bandcomp: BandcompSchema):
    
    link_exten = link_generator(bandcomp.dict().get("email")) #link exten ini sama kayak otpnya
    bandcomp_vote(bandcomp.dict().get("email"), link_exten, bandcomp.dict().get("who"))
    # verif_list.append(link_exten)

    send_email_background(background_tasks, 'Hello World',  # disini title 
    bandcomp.dict().get("email"), link_exten) # disini body

    # print(verif_list)
    # print(link_exten)
    # print(type(email.dict().get("email")[0]))
    # print(email.dict().get("email"))
    return 'Success'

@app.post('/bandcomp/verification')
async def verification(otp : str):
    if searh_bandcomp_otp(otp):
        bandcomp_vote_verificated(otp)
        used_number_delete(int(otp[3:]))
        return {'status' : 'Success'}
    else:
        return {'status' : 'Failed'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)