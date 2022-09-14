from imp import reload
import os
from re import template
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI, BackgroundTasks, status, Response, Request
from fastapi.responses import HTMLResponse
from send_email import send_otp_email_background, send_thanks_email_background
from pydantic import BaseModel, EmailStr
from link_generator import link_generator, used_number_delete

from pymongo import MongoClient
from database import check_email, already_verificated, bandcomp_vote, searh_bandcomp_otp, bandcomp_vote_verificated

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from starlette.exceptions import HTTPException as StarletteHTTPException
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
band_list_db = db.band_list

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# print(Envs.MAIL_USERNAME)

@app.exception_handler(StarletteHTTPException)
async def exception_handler(request: Request, exc: StarletteHTTPException):
    
    if exc.status_code == 404:
        return templates.TemplateResponse('announcement.html', {'request' : request,
                                                                'title': str(exc.status_code) + ' ' + str(exc.detail), 
                                                                'message': "The page you requested was not found."})

    elif exc.status_code == 500:
        return templates.TemplateResponse('announcement.html', {'request' : request,
                                                                'title': str(exc.status_code) + ' ' + str(exc.detail), 
                                                                'message': "Internal server error, please try again later."})
    else:
        # Generic error page
        return templates.TemplateResponse('announcement.html', {'request' : request,
                                                                'title': str(exc.status_code) + ' ' + str(exc.detail), 
                                                                'message': str(exc.status_code) + ' ' + str(exc.detail) + " error"})



@app.get('/', response_class=HTMLResponse)
async def index(request: Request):

    bands = []
    band_list = band_list_db.find()
    for row in band_list:
        bands.append(row)

    # print(bands)

    jinja_var = {'request' : request,
                'bands' : bands}
    return templates.TemplateResponse('index.html', jinja_var)


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
    # print(bandcomp.dict())
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

@app.get('/bandcomp/video')
async def band_video(band_id : int, Response:Response, request: Request):


    # band id dict sama band link dict harus kerja sama jadi harus teliti yyy

    band_id_dict = {}
    band_link_dict = {  "smada big bang" : "yQ67XSO5S2Q",
                        "smada little kids" : "XI0q7L_S2mo",}

    band_list = band_list_db.find()
    x = 0 
    for row in band_list:
        x+=1

        video_link = row['link']
        video_link = video_link.split('youtu.be/')[1]
        band_id_dict[x] = row['name']
        band_link_dict[row['name'].lower()] = video_link 


    

    try :
        band_who= band_id_dict[band_id].lower()

    except:
        Response.status_code = status.HTTP_404_NOT_FOUND
        return templates.TemplateResponse('announcement.html', {'request' : request,
                                                                'title': 'Band Video Not Found',
                                                                'message': 'Already uploaded? Try to contact Admin'})
    try :
        return templates.TemplateResponse('video_template.html', {  'request': request,
                                                                    'title' : band_who,
                                                                    'who' : band_who,
                                                                    'band_link' : band_link_dict[band_who]})
    except:
        Response.status_code = status.HTTP_404_NOT_FOUND
        return templates.TemplateResponse('announcement.html', {'request' : request,
                                                                'title': 'Band Video Not Found',
                                                                'message': 'Already uploaded? Try to contact Admin'})


if __name__ == '__main__':
    uvicorn.run('main:app' ,reload=True)