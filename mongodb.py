import os
from dotenv import load_dotenv
from pymongo import MongoClient

from fastapi import BackgroundTasks

from pydantic import BaseModel
from pydantic.networks import EmailStr

from send_email import send_thanks_email_background
load_dotenv('.env')

client = MongoClient(os.getenv('ATLAS_URI'))
db = client.smadaf
bandcomp_vote_db = db.bandcomp_vote_database
band_list_db = db.band_list 
# print(bandcomp_vote_db)

class Vote(BaseModel) : 
    email : EmailStr
    otp : str  
    who : str
    is_verificated : bool

def bandcomp_vote(email, otp, who):
    vote = Vote(email=email, otp=otp, who=who, is_verificated=False)
    bandcomp_vote_db.insert_one(vote.dict())  

def searh_bandcomp_otp(otp): 
    """search for otp if found and is_verificated is False return True else return false"""
    if bandcomp_vote_db.find_one({"otp": otp, "is_verificated": False}):
        return True
    else:
        return False
    
def already_verificated(otp):
    """search for otp and if found return True else return False"""
    if bandcomp_vote_db.find_one({"otp": otp, "is_verificated": True}):
        return True
    else:
        return False

def del_other_non_verificated(email):
    """search for email in otp and if found delete all other non-verificated"""
    bandcomp_vote_db.delete_many({"email": email, "is_verificated": False})

def bandcomp_vote_verificated(otp):
    """search for otp and if found set is_verificated to True"""
    bandcomp_vote_db.update_one({"otp": otp}, {"$set": {"is_verificated": True}})
    del_other_non_verificated(bandcomp_vote_db.find_one({"otp": otp}).get("email"))
    
def check_email(email) :
    """if email is found in database and is_verificated == True return true else return false"""
    if bandcomp_vote_db.find_one({"email": email, "is_verificated": True}):
        return True
    else:
        return False

band_list = band_list_db.find()
for row in band_list:
    print(row)

