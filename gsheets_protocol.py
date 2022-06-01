import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('.env')

client = MongoClient(os.getenv('ATLAS_URI'))
db = client.smadaf
bandcomp_vote_db = db.bandcomp_vote_database

### MULAI GSHEETS SETUP ###
import pygsheets

gc = pygsheets.authorize(service_file='smadafiestaweb-54799458e73d.json')
sh = gc.open('smada-fiesta-vote')
bandcomp_wks = sh.sheet1

# bandcomp_wks.update_value('A1', 'email')

header = bandcomp_wks.cell('A1')
header.value = 'SBB'
header.text_format['bold'] = True # make the header bold
header.update()

header = bandcomp_wks.cell('B1')
header.value = 'SLB'
header.text_format['bold'] = True # make the header bold
header.update()

# print(bandcomp_wks.cell('A2').value)

### AKHIR GSHEETS SETUP ###



def all_who() : 
    """return all who in mongo db"""
    who = bandcomp_vote_db.distinct("who")
    return who

def count_vote(who) : 
    """count how many vote for who but is_verified must be true"""
    count = bandcomp_vote_db.count_documents({"who": who, "is_verificated": True})
    return count

print(count_vote("SBB"))


"""Nanti jadi klo udah ada banyak vote(maksudnya kyk slb sbb dll bandnya) kita settings semua biar semua entri bisa dimasukin ge gsheets"""