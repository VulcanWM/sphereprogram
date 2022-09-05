import pymongo
import dns
import os
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

loginclient = pymongo.MongoClient(os.getenv("loginclient"))
usersdb = loginclient.Users
profilescol = usersdb.Profiles
questionsclient = pymongo.MongoClient(os.getenv("questionsclient"))

def addcookie(key, value):
  session[key] = value

def delcookie(keyname):
  session.clear()

def getcookie(key):
  try:
    if (x := session.get(key)):
      return x
    else:
      return False
  except:
    return False

def gethashpass(username):
  myquery = { "UN": username }
  mydoc = profilescol.find(myquery)
  for x in mydoc:
    return x['PW']
  return False

def getuserid(id):
  myquery = { "_id": int(id) }
  mydoc = profilescol.find(myquery)
  for x in mydoc:
    return True
  return False

def getuser(username):
  myquery = { "UN": username }
  mydoc = profilescol.find(myquery)
  for x in mydoc:
    if x.get("Deleted", None) == None:
      return x
    return False
  return False

def create_account(username, password, developer):
  username = username.lower()
  if getuser(username) != False:
    return "This is already a username! Pick another one!"
  passhash = generate_password_hash(password)
  document = [{
    "UN": username.lower(),
    "PW": passhash,
    "CR": datetime.datetime.now(),
    "DV": developer,
    "CW": [],
    "PB": [],
    "PT": 0,
    "RL": [],
    "BD": []
  }]
  profilescol.insert_many(document)
  return True