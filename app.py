from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb://farhan:farhan@ac-amvpek4-shard-00-00.fydd3ha.mongodb.net:27017,ac-amvpek4-shard-00-01.fydd3ha.mongodb.net:27017,ac-amvpek4-shard-00-02.fydd3ha.mongodb.net:27017/?ssl=true&replicaSet=atlas-qout9c-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0')
db = client.dblist

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_received = request.form['bucket_give']
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num': num,
        'bucket': bucket_received,
        'done': 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'data saved'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = int(request.form["num_give"])
    db.bucket.update_one(
        {'num': num_receive},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update done!'})

@app.route("/bucket/delete", methods=["POST"]) 
def delete_bucket():
    num_receive = int(request.form["num_give"])
    db.bucket.delete_one({'num': num_receive})
    return jsonify({'msg': 'Item deleted!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({}, {'_id': False})) 
    return jsonify({'buckets': buckets_list}) 

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
