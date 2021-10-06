from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
from flask import Response
app = Flask(__name__)


cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
def sendNotification(usertoken, title, body):
    
    userdata = {
        "to": usertoken,
        "notification": {
            "body": " ".join(str(body).split(" ")[:12])+"... Tap To Read More",
            "title": str(title),
            "content_available": True,
            "priority": "high"
        }

    }
    t="AAAAAXiI6hg:APA91bE2NceIPnT2ZELJzvuOPWqFhi3dIr1ZqXJIS57WK3cCTg7q57qL_vQ6GcOxys7IvxmIySoKpjqh2F1mMlCbq8b3a7gtmUDf-WdhTZyYvQZYzlFdiw5_tmaekkc_TgySReVtq63Z"
    headers = {
        "Authorization": "key="+t,
        "Content-Type": "application/json"

    }
    r = requests.post(
        'https://fcm.googleapis.com/fcm/send',  json=userdata, headers=headers)
    print(r.status_code,usertoken,r.json())


@app.route('/post/', methods=['POST'])
def post_something():
    title = request.form.get('title',"YWCA App")
    body = request.form.get('body',"Intresting events await you")
    password=request.form.get('password',"")

    if password=="12345678":

        doc_ref = db.collection('mobileToken').stream()

        for doc in doc_ref:
            sendNotification(doc.to_dict()["token"],title,body)

        return Response("{'message':'successfull'}", status=201, mimetype='application/json')

    else:
        return Response("{'message':'Check your password'}", status=401, mimetype='application/json')



# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
