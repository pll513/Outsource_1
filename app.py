# coding=utf-8
from flask import Flask, abort, jsonify, url_for, g
from pymongo import MongoClient, DESCENDING
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from bson.objectid import ObjectId
from datetime import datetime
from flask import request, send_from_directory
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class


app = Flask(__name__)
auth = HTTPBasicAuth()
db = MongoClient().Outsource_1
app.config["SECRET_KEY"] = "ohflkfjenfoiehfoiwehjpj"
app.config['UPLOADED_PHOTOS_DEST'] = '/home/www/outsource/static/image/find'  # 文件储存地址

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # 文件大小限制，默认为16MB


@app.route('/api/v1.0/count')
@auth.login_required
def sight_counts():
    results = []
    for find in db.sights.find():
        query = {"loc": {"$within": {"$center": [find['sight_location'], 5/111.12]}}}
        sight_count = db.location.find(query).count()
        results.append({"name": find['name'], "count": sight_count})
    return jsonify(results)


@app.route('/api/v1.0/location_num', methods=["POST"])
@auth.login_required
def post_location_num():
    results = request.json.get('location_num')
    for result in results:
        db.sights.update({'name': result['name']}, {"$set": {"sight_location": result['sight_location']}}, upsert=True)
    return jsonify("success")


@app.route("/api/v1.0/location_num", methods=["GET"])
@auth.login_required
def get_location_num():
    results = []
    for find in db.sights.find():
        results.append({
            'name': find['name'],
            's_location': find['sight_location']
        })
    return jsonify(results)


@app.route('/api/v1.0/uploads', methods=['POST'])
@auth.login_required
def upload_img():
    results = []
    for filename in request.files.getlist('photos'):
        result = photos.save(filename)
        results.append(result)
    return jsonify(results)


@app.route('/api/v1.0/find', methods=['POST'])
@auth.login_required
def post_find():
    find = {
        'name': g.user.name,
        'photos': request.json.get('photos'),
        'content': request.json.get('content'),
        #'date': datetime.now().strftime("%Y-%m-%d"),
        'time': datetime.now(),  #.strftime("%H:%M:%S"),
        'location': request.json.get('location'),
        'like': []
    }
    db.finds.insert(find)
    return jsonify(g.user.name)


@app.route('/api/v1.0/find', methods=['GET'])
@auth.login_required
def get_find():
    results = []
    for find in db.finds.find().sort("time", DESCENDING):
        like_status = True
        if g.user.name in find['like']:
            like_status = False

        result = {
            '_id': str(find['_id']),
            'name': find['name'],
            'photos': ["/static/image/find/" + i for i in find['photos']],
            'content': find['content'],
            'date': find['time'].strftime("%Y-%m-%d"),
            'time': find['time'].strftime("%H:%M:%S"),
            'location': find['location'],
            'like': len(find['like']),
            'like_status': like_status
        }
        results.append(result)
    return jsonify(results)


@app.route('/api/v1.0/like/<string:find_id>', methods=['PUT'])
@auth.login_required
def like(find_id):
    find = db.finds.find_one({'_id': ObjectId(find_id)})
    find['like'].append(g.user.name)
    db.finds.update({'_id': find['_id']}, {"$set": {"like": find['like']}})
    return jsonify(find['content'])


class Users(object):
    def __init__(self, phone="", name="", password=""):
        self.id = ""
        self.phone = phone
        self.name = name
        self.password = password

    def setId(self, user_id):
        self.id = user_id

    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    def generate_auth_token(self, expriation=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expriation)
        return s.dumps({'id': self.phone})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = db.users.find_one({"phone": (data['id'])})
        return Users(phone=user['phone'], password=user['password'], name=user['name'])


@app.route("/")
def index():
    return send_from_directory('/var/www/tour/build', "index.html")


@app.route("/api/v1.0/token", methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token.decode("ascii")})


@app.route("/api/v1.0/location", methods=['POST'])
@auth.login_required
def put_location():
    location = request.json.get('location')
    phone = g.user.phone
    db.location.update({'phone': phone}, {"$set": {"loc": location}}, upsert=True)
    return jsonify(phone)


@app.route('/api/v1.0/location', methods=['GET'])
def get_location():
    results = []
    for result in db.location.find():
        results.append({
            'phone': result['phone'],
            'location': result['location']
        })
    return jsonify(results)


@app.route('/api/v1.0/log_out', methods=['GET'])
@auth.login_required
def log_out():
    phone = g.user.phone
    db.location.delete_one({"phone": phone})
    return jsonify(phone)


@auth.verify_password
def verify_password(phone_or_token, password):
    user = Users.verify_auth_token(phone_or_token)
    if not user:
        user_json = db.users.find_one({"phone": phone_or_token})
        user = Users(user_json['phone'], user_json['name'], user_json['password'])
        if not user_json or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/v1.0/hotel', methods=['POST'])
@auth.login_required
def post_hotel():
    hotel = {
        "name": request.json.get('name'),
        "location": request.json.get('location'),
        "time": request.json.get('time'),
        "level": request.json.get('level'),
        "photo": request.json.get('photo')
    }
    db.hotels.insert(hotel)
    return jsonify(g.user.name)


@app.route('/api/v1.0/hotel', methods=['GET'])
@auth.login_required
def get_hotel():
    results = []
    for result in db.hotels.find():
        result['_id'] = str(result['_id'])
        results.append(result)
    return results


@app.route('/api/v1.0/collection/<string:hotel_id>', methods=['POST'])
@auth.login_required
def post_collection(hotel_id):
    db.collection.insert({
        'phone': g.user.phone,
        'hotel_id': hotel_id
    })
    return jsonify(g.user.phone)


@app.route('/api/v1.0/collection', methods=['GET'])
@auth.login_required
def get_collection():
    phone = g.user.phone
    results = []
    for result in db.collection.find({'phone': phone}):
        hotel = db.hotels.find_one({'_id': ObjectId(result['hotel_id'])})
        hotel_json = {
            'hotel_id': str(hotel['_id']),
            "name": hotel['name'],
            "location": hotel['location'],
            "time": hotel['time'],
            "level": hotel['level'],
            "photo": hotel['photo']
        }
        results.append(hotel_json)
    return jsonify(results)


@app.route('/api/v1.0/collection/<string:hotel_id>', methods=['Delete'])
@auth.login_required
def delete_collection(hotel_id):
    phone = g.user.phone
    db.collection.remove({'phone':phone, 'hotel_id': hotel_id})
    return jsonify(phone)


@app.route("/api/v1.0/password", methods=['PUT'])
@auth.login_required
def change_password():
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')
    if verify_password(g.user.phone, old_password):
        g.user.hash_password(new_password)
        new_password = g.user.password
        db.users.update({'phone': g.user.phone}, {"$set": {"password": new_password}})
    return jsonify(g.user.phone)


@app.route("/api/v1.0/users", methods=["POST"])
def sign_up():
    phone = request.json.get("phone")
    name = request.json.get('name')
    password = request.json.get("password")
    if phone is None or password is None or name is None:
        abort(400)
    if db.users.find_one({"phone": phone}):
        abort(400)
    user = Users(phone, name)
    user.hash_password(password)
    user_json = {
        "phone": phone,
        "name": name,
        "password": user.password
    }
    db.users.insert_one(user_json)
    user.setId(db.users.find_one({'phone': phone})['_id'])
    return jsonify({"phone": user.phone}), 201, {"Location": url_for('sign_in',
                                                                         user_id=str(user.id),
                                                                         _external=True)}


@app.route("/api/v1.0/users/<string:user_id>", methods=['GET'])
def sign_in(user_id):
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        abort(400)
    return jsonify({'phone': user.phone})


@app.route("/api/v1.0/sight", methods=['POST'])
@auth.login_required
def post_sight():
    sight_json = {
        'name': request.json.get('name'),
        'des': request.json.get('des'),
        'photo': request.json.get('photo')
    }
    db.sights.insert(sight_json)
    return jsonify({"name": sight_json['name']}), 201, {"Location": url_for('get_sights',
                                                                            _external=True)}


@app.route("/api/v1.0/sights", methods=["GET"])
def get_sights():
    sights = []
    for sight in db.sights.find():
        result = ["/static/image/sight/" + i for i in sight['photo']]
        sights.append({
            'sight_id': str(sight['_id']),
            'name': sight['name'],
            'des': sight['des'],
            'photo': result
        })
    return jsonify(sights)


@app.route("/api/v1.0/sight/<string:sight_id>", methods=["GET"])
def get_sight(sight_id):
    sight = db.sights.find_one({'_id': ObjectId(sight_id)})
    result = []
    for i in sight['photo']:
        i = "/static/image/sight/" + i
        result.append(i)
    return jsonify({"name": sight['name'],
                    "des": sight['des'],
                    "imgs": result})


@app.route("/api/v1.0/path", methods=["POST"])
@auth.login_required
def post_path():
    sights_name = request.json.get('sights_name')
    path_name = request.json.get('path_name')
    distance = request.json.get('distance')
    sights_id = []
    for sight_name in sights_name:
        sight = db.sights.find_one({"name": sight_name})
        sights_id.append(str(sight['_id']))
    path_json = {
        'name': path_name,
        'sights_id': sights_id,
        'distance': distance
    }
    db.paths.insert(path_json)
    return jsonify({"name": path_json['name']}), 201, {"Location": url_for('get_paths', _external=True)}




@app.route("/api/v1.0/paths", methods=['GET'])
def get_paths():
    paths = []
    for path in db.paths.find():
        length = len(path['sights_id'])
        if length > 3:
            path['sights_id'] = path['sights_id'][:3]
        sights = []
        for sight_id in path['sights_id']:
            sight = db.sights.find_one({'_id': ObjectId(sight_id)})
            if len(sight['photo']) > 0:
                photo = "/static/image/sight/" + sight['photo'][0]
            else:
                photo = ""
            sights.append({
                'name': sight['name'],
                'photo': photo
            })
        paths.append({
            'path_id': str(path['_id']),
            'name': path['name'],
            'sights': sights
        })
    return jsonify(paths)


@app.route('/api/v1.0/path/<string:path_id>', methods=['GET'])
def get_path(path_id):
    path = db.paths.find_one({"_id": ObjectId(path_id)})
    result = {'sights': [], 'distance': path['distance']}
    for sight_id in path['sights_id']:
        sight = db.sights.find_one({'_id': ObjectId(sight_id)})
        result['sights'].append({
            'sight_id': str(sight['_id']),
            'name': sight['name'],
            'des': sight['des']
        })
    return jsonify(result)


@app.route("/api/v1.0/article", methods=['POST'])
@auth.login_required
def post_article():
    article_json = {
        "name": request.json.get('name'),
        'type': request.json.get('type'),
        'date': datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        'content': request.json.get('content'),
        'photos': request.json.get('photos'),
        'readtimes': 0
    }
    db.articles.insert(article_json)
    return jsonify({"name": article_json['name']}), 201, {"Location": url_for('get_articles', _external=True)}


@app.route('/api/v1.0/articles', methods=["GET"])
def get_articles():
    results = []
    for article in db.articles.find():
        result = {
            '_id': str(article['_id']),
            'name': article['name'],
            'type': article['type'],
            'date': article['date'],
            'readtimes': article['readtimes'],
            'photos': article['photos']
        }
        results.append(result)
    return jsonify(results)


@app.route("/api/v1.0/article/<string:article_id>", methods=['GET'])
def get_article(article_id):
    article = db.articles.find_one({'_id': ObjectId(article_id)})
    article['readtimes'] += 1
    db.articles.update({'_id': article['_id']}, {"$set": {"readtimes": article['readtimes']}})
    article['_id'] = str(article['_id'])
    return jsonify(article)


@app.route('/api/v1.0/folkways', methods=['GET'])
def get_folkways():
    results = []
    for article in db.articles.find({"type": "特色名俗"}):
        result = {
            '_id': str(article['_id']),
            'name': article['name'],
            'type': article['type'],
            'date': article['date'],
            'readtimes': article['readtimes'],
            'photos': article['photos'],
            'content': article['content']
        }
        results.append(result)
    return jsonify(results)


@app.route('/api/v1.0/tibet', methods=['GET'])
def get_tibet():
    results = []
    for article in db.articles.find({"type": "特色藏风"}):
        result = {
            '_id': str(article['_id']),
            'name': article['name'],
            'type': article['type'],
            'date': article['date'],
            'readtimes': article['readtimes'],
            'photos': article['photos'],
            'content': article['content']
        }
        results.append(result)
    return jsonify(results)


@app.route('/api/v1.0/red_classics', methods=['GET'])
def get_red_classics():
    results = []
    for article in db.articles.find({"type": "红色经典"}):
        result = {
            '_id': str(article['_id']),
            'name': article['name'],
            'type': article['type'],
            'date': article['date'],
            'readtimes': article['readtimes'],
            'photos': article['photos'],
            'content': article['content']
        }
        results.append(result)
    return jsonify(results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

