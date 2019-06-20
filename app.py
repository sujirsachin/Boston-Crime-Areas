from base64 import b64encode

import bson
import gridfs

from flask import Flask, render_template, request, url_for, session
from flask_pymongo import PyMongo, MongoClient
from flask import Flask, request, redirect, url_for, make_response, abort


from gridfs import GridFS


DB = MongoClient().gridfs_server_test
FS = GridFS(DB)
global data
from gridfs import GridFS, NoFile
from bson.objectid import ObjectId
from flask import make_response
app = Flask(__name__)
db=app.config['MONGO_DBNAME'] = 'BostonCrimeDatabase'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/BostonCrimeDatabase'
mongo = PyMongo(app)
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['BostonCrimeDatabase']
grid_fs = GridFS(db)
def img(obj_id):
    grid_fs_file = grid_fs.find_one({'_id': obj_id})
    response = make_response(grid_fs_file.read())
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename={}".format(obj_id)
    return response
@app.route('/')
def index():

    return render_template('index.html')
@app.route('/home')
def home():
    return render_template('search.html')

@app.route('/details',methods=['GET'])
def details():
    global data
    images={}
    if request.method == 'GET':

	    d = request.args.get('message')



    global regx
    data=d.upper()
    regx=bson.regex.Regex('^'+data+'')
    offence= mongo.db.Crimes.find({"STREET":regx},{'Lat':0,'Long':0,'_id':0}).limit(160)
    street= mongo.db.Crimes.find({"STREET":regx},{'STREET':1,'_id':0}).limit(1)
    date= mongo.db.Crimes.find({"STREET":regx},{'OCCURRED_ON_DATE':1,'_id':0}).limit(5)
    id= mongo.db.Crimes.find({"STREET":regx},{"Image_Id":1,"_id":0}).limit(1)
    street=db.Crimes.find({'STREET':regx}).limit(1)

    item_count = mongo.db.Crimes.count_documents({"STREET": regx})
    if item_count!=0:
        for im in id:
            ob=im['Image_Id']
        fs = gridfs.GridFS(db)
        oid2 = ObjectId(ob)

        for grid in fs.find({"_id":oid2}):
            print(grid)
            img=b64encode(grid.read()).decode('utf-8')

        return render_template('details.html',data=street,offence=offence,street=street,date=date,count=item_count,img=img)
    else:
        return redirect(url_for('home',_anchor='my_anchor1'))
@app.route('/comments',methods=['GET'])
def comments():

    global regx
    if request.method == 'GET':
	    comm = request.args.get('comments')
    street=db.Crimes.find({'STREET':regx}).limit(1)


    if comm:
        da=comm

        for st in street:
            street1=st['STREET']
        mongo.db.Comments.insert({"Street":street1,"Comment":da})
        com=mongo.db.Comments.find({"Street":street1},{"Comment":1,"_id":0})

        return render_template('comments.html',com=com,street=street)
    else:
        for st in street:
            street1=st['STREET']
        com=mongo.db.Comments.find({"Street":street1},{"Comment":1,"_id":0})

        return render_template('comments.html',com=com,street=street)

@app.route('/map')
def map():
    global data
    global regx
    lat = mongo.db.Crimes.find({'STREET':regx},{'Lat':1,'_id':0}).limit(1)
    long= mongo.db.Crimes.find({'STREET':regx},{'Long':1,'_id':0}).limit(1)
    lat1=mongo.db.Crimes.find({'STREET':regx}).limit(5)
    item_count = mongo.db.Crimes.count_documents({"STREET":regx})
    street=db.Crimes.find({'STREET':regx},{'Lat':0,'Long':0,'OFFENSE_CODE_GROUP':0,'OCCURRED_ON_DATE':0,'Image_Id':0,'_id':0}).limit(1)
    for st in street:
        str=st['STREET']

    return render_template('map.html', lat=lat,long=long,data=data,street=str,count=item_count,lat2=lat1)

@app.route('/myredirect')
def my_redirect():
    return redirect(url_for('index',_anchor='my_anchor'))
@app.route('/myredirect1')
def my_redirect1():
    return redirect(url_for('home',_anchor='my_anchor1'))
app.run(debug=True)
#app.run('0.0.0.0',80,debug=True)
