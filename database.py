import email
import os
from unittest import result
from dotenv import load_dotenv
load_dotenv('.env')

import pymysql


mysql_host = "localhost"

bandlist_db = pymysql.connect(  host = mysql_host,
                                user = os.getenv('MY_SQL_USER'),
                                password = os.getenv('MY_SQL_PASS'),
                                database = "smadafie_band_list_database")
votelist_db = pymysql.connect(  host = mysql_host,
                                user = os.getenv('MY_SQL_USER'),
                                password = os.getenv('MY_SQL_PASS'),
                                database = "smadafie_vote_database")

vote_cursor = votelist_db.cursor(pymysql.cursors.DictCursor)
band_cursor = bandlist_db.cursor(pymysql.cursors.DictCursor)

def bandcomp_vote(email, otp, who):
    is_verificated = 0
    insert_query =  """insert into vote(email, otp, who, is_verificated) values("%s", "%s", "%s", "%s")"""\
                    %(email, otp, who, is_verificated)

    try :
        vote_cursor.execute(insert_query)
        votelist_db.commit()
    except Exception as e :
        print(e)

def searh_bandcomp_otp(otp): 
    """search for otp if found and is_verificated is False return True else return false"""
    vote_query = """select * from vote where otp = "%s" and is_verificated = 0"""%(otp)
    vote_cursor.execute(vote_query)
    result = vote_cursor.fetchall()

    if result:
        return True
    else:
        return False

def already_verificated(otp):
    """search for otp and if found and is verificate true return True else return False"""
    vote_query = """select * from vote where otp = "%s" and is_verificated = 1"""%(otp)
    vote_cursor.execute(vote_query)
    result = vote_cursor.fetchall()

    if result:
        return True
    else:
        return False

def del_other_non_verificated(email):
    """search for email in otp and if found delete all other non-verificated"""
    vote_query = """delete from vote where email = "%s" and is_verificated = 0"""%(email)
    vote_cursor.execute(vote_query)
    votelist_db.commit()

def bandcomp_vote_verificated(otp):
    """search for otp and if found set is_verificated to True"""
    vote_query = """update vote set is_verificated = 1 where otp = "%s" """%(otp)
    vote_cursor.execute(vote_query)
    votelist_db.commit()
    
    email_query= """select email from vote where otp = "%s" """%(otp)
    vote_cursor.execute(email_query)
    email = vote_cursor.fetchall()
    email = email[0]['email']
    del_other_non_verificated(email)

def check_email(email) :
    """if email is found in database and is_verificated == True return true else return false"""
    vote_query = """select * from vote where email = "%s" and is_verificated = 1"""%(email)
    vote_cursor.execute(vote_query)
    result = vote_cursor.fetchall()
    if result:
        return True
    else:
        return False



# otp="123456"
# who_query = """select who from vote where otp = %s"""%(otp)
# vote_cursor.execute(who_query)
# who = vote_cursor.fetchall()
# who = who[0]['who']

# email_query = """select email from vote where otp = %s"""%(otp)
# vote_cursor.execute(email_query)
# email = vote_cursor.fetchall()
# email = email[0]['email']


# print(who, email)

# band_query = "select * from band_list"

# try :
#     band_cursor.execute(band_query)
#     result = band_cursor.fetchall()
#     for row in result :
#         print(row)
# except Exception as e :
#     print(e)

# bandcomp_vote_verificated("ini8390280")