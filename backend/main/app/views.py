from datetime import datetime
from app import app
from app import database
from flask import redirect
from flask import request
from flask import jsonify
from flask import url_for
from pymongo import MongoClient
from app import ma
import os
import json

class MemeDB(database.Model):
  id = database.Column(database.Integer, primary_key=True)
  name = database.Column(database.String(255))
  caption = database.Column(database.String(255))
  url = database.Column(database.String(255))
  dateTime = database.Column(database.DateTime, default=datetime.now)


class MemeSchema(ma.Schema):
  class Meta:
    fields = ('id','name','caption','url')

meme_schema = MemeSchema()
memes_schema = MemeSchema(many=True)

class Mongo():
    
  def insertToDB(self,name="Anonymous",caption="N/A",url="N/A"):
    try:
      
      newRow = MemeDB(name=name,caption=caption,url=url)
      database.session.add(newRow)
      database.session.commit()
      return {"id":newRow.id}
    except:
      return {"error":"Databse is not available right now."}

  def getMemes(self):
    try:
      
      allMemes = MemeDB.query.order_by(MemeDB.dateTime.desc()).all()
      result = memes_schema.dump(allMemes)
      return jsonify(result)
    except:
      return {"error":"Databse is not available right now.."}

  def getMemeById(self,postId):
    try:
      # database.session.query(MemeDB).delete()
      # database.session.commit()
      meme = MemeDB.query.get(postId)
      if(meme):
        return meme_schema.jsonify(meme)
      else:
        return {"error":"404"}

    except:
      return {"error":"Databse is not available right now."}


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
