import os
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials, firestore

from pydantic import BaseModel
from pydantic.networks import EmailStr

load_dotenv('.env')

firebase_key = {
    "type": "service_account",
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace("\\n", "\n"),
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('CLIENT_ID'),
    "auth_uri": os.getenv('AUTH_URI'),
    "token_uri": os.getenv('TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.getenv('CLIENT_X509_CERT_URL')
}

cred = credentials.Certificate(firebase_key)
firebase_admin.initialize_app(cred)
db=firestore.client()

bandcomp_vote_db = db.collection('vote')

class Vote(BaseModel) : 
    email : EmailStr
    otp : str  
    who : str
    is_verificated : bool

def bandcomp_vote(email, otp, who):
    vote = Vote(email=email, otp=otp, who=who, is_verificated=False)
    bandcomp_vote_db.add(vote.dict())

def searh_bandcomp_otp(otp): 
    """search for otp if found and is_verificated is False return True else return false"""
    if bandcomp_vote_db.where("otp", "==", otp).where("is_verificated", "==", False).get():
        return True
    else:
        return False

def already_verificated(otp): 
    """search for otp and if found return True else return False"""
    if bandcomp_vote_db.where("otp", "==", otp).where("is_verificated", "==", True).get():
        return True
    else:
        return False

def del_other_non_verificated(email):
    """search for email in otp and if found delete all other non-verificated"""
    false_vote = bandcomp_vote_db.where("email", "==", email).where("is_verificated", "==", False).stream()
    for vote in false_vote:
        vote.delete()


    # delete_many({"email": email, "is_verificated": False})


del_other_non_verificated("echoind1945@gmail.com")

# print(searh_bandcomp_otp('123456'))
# print(already_verificated('123456'))
# test= Vote(email="echoind1945@gmail.com", otp="21223457", who="band1", is_verificated=False)
# bandcomp_vote_db.add(test.dict())