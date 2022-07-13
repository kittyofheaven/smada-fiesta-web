import os
from re import template
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI, BackgroundTasks, status, Response, Request
from send_email import send_otp_email_background, send_thanks_email_background
from pydantic import BaseModel, EmailStr
from link_generator import link_generator, used_number_delete

from pymongo import MongoClient
from database import check_email, already_verificated, bandcomp_vote, searh_bandcomp_otp, bandcomp_vote_verificated

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")
### TODO LIST ###
# buat link yg dikirim ke pengguna itu jadi dalam bentuk yang pasti
# html buat email
# integrasi html email ke app fastapi
# mekanisme voting

load_dotenv('.env')

app = FastAPI()
client = MongoClient(os.getenv('ATLAS_URI'))
db = client.smadaf
bandcomp_vote_db = db.bandcomp_vote_database

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
def send_email_backgroundtasks(background_tasks: BackgroundTasks,Response:Response, bandcomp: BandcompSchema):
    
    if check_email(bandcomp.dict().get("email")):
        Response.status_code = status.HTTP_409_CONFLICT
        return {'status' : "Email already used please use another email"}
    
    link_exten = link_generator(bandcomp.dict().get("email")) #link exten ini sama kayak otpnya
    bandcomp_vote(bandcomp.dict().get("email"), link_exten, bandcomp.dict().get("who"))
    # verif_list.append(link_exten)

    send_otp_email_background(background_tasks, 'Confirm vote for Bandcomp 2k22',  # disini title 
    bandcomp.dict().get("email"), link_exten, bandcomp.dict().get("who")) # disini body

    # print(verif_list)
    # print(link_exten)
    # print(type(email.dict().get("email")[0]))
    # print(email.dict().get("email"))
    return {'status' : 'Success'}

@app.get('/bandcomp/verification')
async def verification(otp : str, Response:Response, background_tasks: BackgroundTasks, request: Request):
    if searh_bandcomp_otp(otp):

        who = bandcomp_vote_db.find_one({"otp": otp}).get("who")
        email = bandcomp_vote_db.find_one({"otp": otp}).get("email")

        name=email.split('@')
        name=name[0].capitalize()

        send_thanks_email_background(background_tasks, email , who)

        bandcomp_vote_verificated(otp)
        used_number_delete(int(otp[3:]))
        return templates.TemplateResponse('announcement.html', {'request' : request,
                                                                'title': 'Thankyou for voting', 
                                                                'message': f"Hi { name }. Thanks for your vote in Bandcomp 2k22! Your vote to { who } will be recorded."})

    elif already_verificated(otp):
        Response.status_code = status.HTTP_409_CONFLICT
        return templates.TemplateResponse('announcement.html', {'request' : request,
                                                                'title': 'Already Verificated', 
                                                                'message': 'You have already verificated your vote'})
    else:
        Response.status_code = status.HTTP_404_NOT_FOUND
        return templates.TemplateResponse('announcement.html', {'request' : request,
                                                                'title': 'Otp Not Found',
                                                                'message': 'Your otp cant be found in database, try re-vote or contact admin'})

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)