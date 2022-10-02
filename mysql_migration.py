import os
from dotenv import load_dotenv
from requests import delete
load_dotenv('.env')

import pymysql
from pydantic import BaseModel
from pydantic.networks import EmailStr

mysql_host = "localhost"

bandlist_db = pymysql.connect(  host = mysql_host,
                                user = "root",
                                password = "Copperkey9?",
                                database = "smadafie_band_list_database")
votelist_db = pymysql.connect(  host = mysql_host,
                                user = "root",
                                password = "Copperkey9?",
                                database = "smadafie_vote_database")

vote_cursor = votelist_db.cursor()
band_cursor = bandlist_db.cursor()

band_delete_existing_table = "drop table if exists band_list"
vote_delete_existing_table = "drop table if exists vote"

create_band_table = """create table band_list(
    _id int not null auto_increment primary key,
    name varchar(50) not null,
    image varchar(500) not null
    )""";

create_vote_table = """create table vote(
    _id int not null auto_increment primary key,
    email varchar(255) not null,
    otp varchar(15) not null,
    who varchar(115) not null,
    is_verificated boolean not null
    )""";

# CREATING TABLES
try :
    band_cursor.execute(band_delete_existing_table)
    print('band table deleted')
    vote_cursor.execute(vote_delete_existing_table)
    print('vote table deleted')

    band_cursor.execute(create_band_table)
    print('band table created')
    vote_cursor.execute(create_vote_table)
    print('vote table created')

except Exception as e :
    print(e)

class Vote(BaseModel) : 
    email : EmailStr
    otp : str  
    who : str
    is_verificated : bool

from pymongo import MongoClient
client = MongoClient(os.getenv('ATLAS_URI'))
db = client.smadaf
bandcomp_vote_db = db.bandcomp_vote_database
band_list_db = db.band_list 

band_list = band_list_db.find()
for row in band_list:
    # print(row['name'], row['image'])
    name = row['name']
    image = "images/band_logo/" + name +".png"
    
    insert_query =  """insert into band_list(name, image) values("%s", "%s")"""\
                    %(name, image)
    
    # print (insert_query)

    try :
        band_cursor.execute(insert_query)
        bandlist_db.commit()
        print(insert_query + 'inserted')
    
    except Exception as e :
        print(e)
        
    



# close connection
bandlist_db.close()
votelist_db.close()


