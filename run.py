from urllib import response
from flask import Flask, request, session, jsonify
import sys
import re
import os
from datetime import datetime, timedelta
import random, string
import hashlib
sys.path.append(os.getcwd())
from config import Config
from functools import wraps
import jwt
import requests
import json
from models import init_app
from sqlalchemy.exc import IntegrityError

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

init_app(app)

def token_required(func):

    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.form.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        except:
            return jsonify({'Alert!': 'Invalid token'}), 403
        
        expiration = datetime.strptime(data['expiration'], "%Y-%m-%d %H:%M:%S.%f")
        if expiration < datetime.now():
            return jsonify({'Message': 'Token expired'}), 403
        return func(*args, **kwargs)
    return decorated


@app.route('/registration', methods=['POST'])  
def registration():
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')
    email = request.form.get('email')

    if None in [username, password, name, email]:
        return jsonify({'Message': 'Bad request, empty field'}), 400

    if not (username.isalnum() and password.isalnum() and name.isalnum()):
        return jsonify({'Message': 'Bad request, wrong input format'}), 400

    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if not re.fullmatch(regex, email):
        return jsonify({'Message': 'Bad request, wrong input format'}), 400

    hash_object = hashlib.sha1(password.encode())
    hex_dig = hash_object.hexdigest()
    
    referral_code = username + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
    with app.app_context():
        from models.database import Session, Users
    db_session = Session()

    ##### try non unique username or email later
    user = Users(username=username, password=hex_dig, name=name, email=email, referral_code=referral_code)
    db_session.add(user)
    try:
        db_session.commit()
    except IntegrityError:
        return jsonify({'Message': 'Bad request, username or email already registred'}), 400
    return jsonify({'Message': 'New user registred'}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if None in [username, password]:
        return jsonify({'Message': 'Bad request, empty field'}), 400
    if not username.isalnum() and password.isalnum():
        return jsonify({'Message': 'Bad request, wrong input format'}), 400
    with app.app_context():
        from models.database import Session, Users
    db_session = Session()

    ##### try add case on no user found
    stored_password = db_session.query(Users.password).filter_by(username=username).all()[0]
    hash_object = hashlib.sha1(password.encode())
    hex_dig = hash_object.hexdigest()
    if not hex_dig == stored_password[0]:
        return jsonify({'Message': 'Wrong password'}), 400

    token = jwt.encode({
        'user': request.form['username'],
        'expiration': str(datetime.utcnow() + timedelta(minutes=30))
        },
        app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token, 'username':username}), 200


### user edit name, or email
@app.route('/edit_data', methods=['POST'])
@token_required
def edit_data():
    param = request.form.get('param_changed')
    new_data = request.form.get(param)
    referral_code = request.form.get('referral_code')

    if None in [param, new_data, referral_code]:
        return jsonify({'Message': 'Bad request, empty field'}), 400

    if param in ['username', 'name', 'password']:
        if not new_data.isalnum():
            return jsonify({'Message': 'Bad request, wrong input format'}), 400
        if param == 'password':
            hash_object = hashlib.sha1(new_data.encode())
            new_data = hash_object.hexdigest()
    else:
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex, new_data):
            return jsonify({'Message': 'Bad request, wrong input format'}), 400
    
    with app.app_context():
        from models.database import Users, Session

    db_session = Session()
    user = db_session.query(Users).filter_by(referral_code=referral_code).first()

    ### verify again this method
    setattr(user, param, new_data)
    db_session.add(user)
    try:
        db_session.commit()
    except IntegrityError:
        return jsonify({'Message': 'Bad request, username or email already registred'}), 400
    return jsonify({'Message': 'Data has successfully changed'}), 200

@app.route('/find_user', methods=['POST'])
def find_user():
    name = request.form.get('name')

    if name is None or not name.isalnum():
        return  jsonify({'Message': 'Bad request, empty field'}), 400
    with app.app_context():
        from models.database import Users, Session
    
    db_session = Session()
    users = db_session.query(Users.name).filter(Users.name.like('%' + name + '%')).all()
    if not users:
        return  jsonify({'Message': 'No user found'}), 200
    else:
        list_user_names = [i[0] for i in users]
        return jsonify({'users': list_user_names}), 200
        
@app.route('/get_hero', methods=['POST'])
def get_hero():
    sub_hero_name = request.form.get('sub_hero_name')

    if sub_hero_name is None:
        return  jsonify({'Message': 'Bad request, empty field'}), 400
    
    url = 'https://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json'
    try:
        response = requests.get(url)
    except requests.ConnectionError:
        return jsonify({'Message': 'Request timeout'}), 408
    
    json_response = response.text
    data = json.loads(json_response)
    data_hero = data['data']
    hero_ids = list(data_hero.keys())

    matched = [hero_id for hero_id in hero_ids if sub_hero_name in hero_id]
    if not matched:
        hero_names = [hero['name'] for hero in data_hero.values()]
        matched = [hero_name for hero_name in hero_names if sub_hero_name in hero_name]
        
        if not matched:
            return jsonify({'Message': 'Hero not found'}), 200
        hero_index = hero_names.index(matched[0])

        return jsonify(data_hero[hero_names[hero_index]]), 200

    return jsonify(data_hero[matched[0]]), 200

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host="0.0.0.0")