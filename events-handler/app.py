from flask import Flask, request, render_template, url_for, jsonify, session
from werkzeug.utils import redirect
from werkzeug.exceptions import abort
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost/events_handler'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'llave_secreta'
users = [
    {
        "email": "a@gmail.com",
        "pwd": "1",
        "events": [
            {
                "name": "a",
                "category": "a",
                "place": "a",
                "address": "a"
            },
            {
                "name": "b",
                "category": "b",
                "place": "b",
                "address": "b"
            }
        ]
    },
    {
        "email": "b@gmail.com",
        "pwd": "1",
        "events": [
            {
                "name": "",
                "category": "",
                "place": "",
                "address": ""
            }
        ]
    },
    {
        "email": "c@gmail.com",
        "pwd": "1",
        "events": [
            {
                "name": "",
                "category": "",
                "place": "",
                "address": ""
            }
        ]
    },
    {
        "email": "d@gmail.com",
        "pwd": "1",
        "events": [
            {
                "name": "",
                "category": "",
                "place": "",
                "address": ""
            }
        ]
    }
]


db = SQLAlchemy(app)
ma = Marshmallow(app)


class Users(db.Model):
    email = db.Column(db.String(100), primary_key=True)
    pwd = db.Column(db.String(100), nullable=False)

    def __init__(self, email, pwd):
        self.email = email
        self.pwd = pwd


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    place = db.Column(db.String(100))
    address = db.Column(db.String(100))
    user_email = db.Column(db.String(100), db.ForeignKey('users.email'))
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    def __init__(self, id, name, category, place, address, user_email, created_at):
        self.id = id
        self.name = name
        self.category = category
        self.place = place
        self.address = address
        self.user_email = user_email
        self.created_at = created_at


db.create_all()


class UserSchema(ma.Schema):
    class Meta:
        fields = ('email', 'pwd')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class EventSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'category', 'place', 'address', 'user_email', 'created_at')


event_schema = EventSchema()
events_schema = EventSchema(many=True)


@app.route('/signups', methods=['PUT'])
def create_task():
    new_email = request.json['email']
    new_pwd = request.json['pwd']
    new_user = Users(new_email, new_pwd)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


@app.route('/validate-pwds', methods=['POST'])
@cross_origin()
def validate_users():
    print(request.get_json())
    email_received = request.json['email']
    pwd_received = request.json['pwd']
    user_validated = Users.query.with_entities(Users.pwd).filter_by(email=email_received)
    pwd_validated = user_validated.scalar()
    response = None
    print(email_received)
    print(pwd_received)
    if pwd_received == pwd_validated:
        response = Users.query.with_entities(Users.email).filter_by(email=email_received)
    else:
        x = [{}]
    # if pwd
    # user = Users.query.get(email)
    return users_schema.jsonify(response)


@app.route('/user-events/<email>', methods=['GET', 'POST'])
@cross_origin()
def user_events(email):
    events = Events.query.order_by(Events.created_at.desc()).filter_by(user_email=email)
    print(events)
    return events_schema.jsonify(events)


@app.route('/event/<id>', methods=['GET', 'POST'])
@cross_origin()
def event(id):
    events = Events.query.filter_by(id=id)

    return events_schema.jsonify(events)


@app.route('/create-event', methods=['GET', 'POST'])
@cross_origin()
def create_event():

    new_name = request.json['name']
    new_category = request.json['category']
    new_place = request.json['place']
    new_address = request.json['address']
    email = request.json['email']
    new_event = Events(None, new_name, new_category, new_place, new_address, email, None)

    db.session.add(new_event)
    db.session.commit()

    return event_schema.jsonify(new_event)


@app.route('/edit-event/<event_id>', methods=['GET', 'POST'])
@cross_origin()
def edit_event(event_id):
    new_name = request.json['name']
    new_category = request.json['category']
    new_place = request.json['place']
    new_address = request.json['address']
    email = Events.query.with_entities(Events.user_email).filter_by(id=event_id)
    user_email = email.scalar()
    print(request.get_json())
    Events.query.filter_by(id=event_id).update(
        {
            Events.name: new_name,
            Events.category: new_category,
            Events.place: new_place,
            Events.address: new_address
        }
    )
    db.session.commit()
    events = Events.query.filter_by(user_email=user_email)
    return events_schema.jsonify(events)


@app.route('/delete-event/<event_id>/', methods=['GET', 'POST'])
@cross_origin()
def delete_event(event_id):
    email = Events.query.with_entities(Events.user_email).filter_by(id=event_id)
    user_email = email.scalar()
    Events.query.filter_by(id=event_id).delete()
    db.session.commit()
    events = Events.query.filter_by(user_email=user_email)
    print(events)
    return events_schema.jsonify(events)


@app.route('/salir')
def salir():
    return abort(404)


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('error404.html', error=error), 404
