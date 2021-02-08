from app import app
from flask import redirect
from flask import request
from flask import url_for
from pymongo import MongoClient
import os
import json

class Mongo():
  def __init__(self):
    DATABASE_URL = os.getenv("DATABASE_URL")
    self.cluster = MongoClient(DATABASE_URL)
    self.db = self.cluster["xmemeDB"]
    self.collection = self.db["xmemeDB"]
  
  def getPostIdNumber(self):
    results = self.collection.find({})
    ids = []
    for result in results:
      ids.append(result["_id"])
    post_id = max(ids)
    post_id += 1
    return post_id
  
  def insertToDB(self,name="Anonymous",caption="N/A",url="N/A"):
    post_id = self.getPostIdNumber()
    post = {"_id":post_id,"name":name,"caption":caption,"url":url}
    self.collection.insert_one(post)
    
    return {"id":post['_id']}
  
  def getMemes(self):
    results = self.collection.find({})
    allMemes = []
    for meme in results:
      allMemes.append(meme)
    allMemes.reverse()
    allMemes = allMemes[:100]
    return json.dumps(allMemes)
  
  def getMemeById(self,postId):
    result = self.collection.find_one({"_id":postId})
    if(result == None):
      return {"error":"404"}
    else:
      return json.dumps(result)


@app.route("/memes",methods = ['POST','GET'])
def index():
  if request.method == 'POST':    
    #check if all 3 params are set
    name = request.args.get('name')
    caption = request.args.get('caption')
    url = request.args.get('url')
    
    mongoObj = Mongo()
    return mongoObj.insertToDB(name,caption,url)
  else:    
    mongoObj = Mongo()
    return mongoObj.getMemes()

@app.route("/memes/<int:postId>",methods = ['GET'])
def getPost(postId=None):
  if(postId != None and request.method == 'GET'):
    mongoObj = Mongo()
    return mongoObj.getMemeById(postId)
