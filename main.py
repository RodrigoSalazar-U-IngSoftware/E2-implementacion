from email import message
from pydoc_data.topics import topics
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from os import path

# CONFIG
DB_NAME = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = "UABFPIUFABIBSAKJFBNDSOUY"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

# DATABASE MODELS
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(256))
    topic = db.Column(db.String(32))

def create_database(app):
    if not path.exists('./'+DB_NAME):
        db.create_all(app=app)
        print("DATABASE CREATED")

# API ENDPOINTS
@app.route('/message',methods=['POST'])
def post_message():
    try:
        json = request.get_json()
        message = json["message"]
        topic = json["topic"]
        ms = Message(message=message, topic=topic)
        db.session.add(ms)
        db.session.commit()
    except:
        return jsonify({
            "status":"fail"
        })

    return jsonify({
        "status":"ok"
    })

@app.route('/message/<topic>',methods=['GET'])
def get_message(topic):
    
    ms_query = Message.query.filter_by(topic=topic).all()

    ms_list = [
        {
            "message": ms.message,
            "topic": ms.topic
        }
        for ms in ms_query
    ]

    return jsonify(ms_list)

# EXECUTE
if __name__ == '__main__':
    create_database(app)
    app.run(host='localhost',port=5002,debug=True)