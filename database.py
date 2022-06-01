import os
from dotenv import load_dotenv
from pymongo import MongoClient

from pydantic import BaseModel
from pydantic.networks import EmailStr

load_dotenv('.env')

client = MongoClient(os.getenv('ATLAS_URI'))
db = client.smadaf
bandcomp_vote_db = db.bandcomp_vote_database

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
    """search for otp if found return true but if not found return false"""
    if bandcomp_vote_db.find_one({"otp": otp}):
        return True
    else:
        return False


def bandcomp_vote_verificated(otp):
    """search for otp and if found set is_verificated to True"""
    bandcomp_vote_db.update_one({"otp": otp}, {"$set": {"is_verificated": True}})

# bandcomp_vote("hazelhandrata@gmail.com", "2234567", "SBB")
# print(searh_otp("123123"))