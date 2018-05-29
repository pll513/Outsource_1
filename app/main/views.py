from . import main
from .. import auth
from flask import request, abort, jsonify, g, url_for
from .. import db, photos
from bson import ObjectId
from datetime import datetime
from pymongo import DESCENDING


@main.route('/api/v1.0/count')
def sight_counts():
    results = []
    for find in db.sights.find():
        query = {"loc": {"$within": {"$center": [find['sight_location'], 5/111.12]}}}
        sight_count = db.location.find(query).count()
        results.append({"name": find['name'], "count": sight_count})
    return jsonify(results)


@main.route('/api/v1.0/location_num', methods=["POST"])
@auth.login_required
def post_location_num():
    results = request.json.get('location_num')
    for result in results:
        db.sights.update({'name': result['name']}, {"$set": {"sight_location": result['sight_location']}}, upsert=True)
    return jsonify("success")


@main.route("/api/v1.0/location_num", methods=["GET"])
@auth.login_required
def get_location_num():
    results = []
    for find in db.sights.find():
        results.append({
            'name': find['name'],
            's_location': find['sight_location']
        })
    return jsonify(results)


@main.route('/api/v1.0/uploads', methods=['POST'])
@auth.login_required
def upload_img():
    results = []
    for filename in request.files.getlist('photos'):
        result = photos.save(filename)
        results.append(result)
    return jsonify(results)


@main.route('/api/v1.0/find', methods=['POST'])
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


@main.route('/api/v1.0/find', methods=['GET'])
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


@main.route('/api/v1.0/like/<string:find_id>', methods=['PUT'])
@auth.login_required
def like(find_id):
    find = db.finds.find_one({'_id': ObjectId(find_id)})
    find['like'].append(g.user.name)
    db.finds.update({'_id': find['_id']}, {"$set": {"like": find['like']}})
    return jsonify(find['content'])


@main.route("/api/v1.0/location", methods=['POST'])
@auth.login_required
def put_location():
    location = request.json.get('location')
    phone = g.user.phone
    db.location.update({'phone': phone}, {"$set": {"loc": location}}, upsert=True)
    return jsonify(phone)


@main.route('/api/v1.0/location', methods=['GET'])
def get_location():
    results = []
    for result in db.location.find():
        results.append({
            'phone': result['phone'],
            'location': result['loc']
        })
    return jsonify(results)


@main.route('/api/v1.0/hotel', methods=['POST'])
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


@main.route('/api/v1.0/hotel', methods=['GET'])
@auth.login_required
def get_hotel():
    results = []
    for result in db.hotels.find():
        result['_id'] = str(result['_id'])
        results.append(result)
    return results


@main.route('/api/v1.0/collection/<string:hotel_id>', methods=['POST'])
@auth.login_required
def post_collection(hotel_id):
    db.collection.insert({
        'phone': g.user.phone,
        'hotel_id': hotel_id
    })
    return jsonify(g.user.phone)


@main.route('/api/v1.0/collection', methods=['GET'])
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


@main.route('/api/v1.0/collection/<string:hotel_id>', methods=['Delete'])
@auth.login_required
def delete_collection(hotel_id):
    phone = g.user.phone
    db.collection.remove({'phone':phone, 'hotel_id': hotel_id})
    return jsonify(phone)


@main.route("/api/v1.0/sight", methods=['POST'])
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


@main.route("/api/v1.0/sights", methods=["GET"])
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


@main.route("/api/v1.0/sight/<string:sight_id>", methods=["GET"])
def get_sight(sight_id):
    sight = db.sights.find_one({'_id': ObjectId(sight_id)})
    result = []
    for i in sight['photo']:
        i = "/static/image/sight/" + i
        result.append(i)
    return jsonify({"name": sight['name'],
                    "des": sight['des'],
                    "imgs": result})


@main.route("/api/v1.0/path", methods=["POST"])
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


@main.route("/api/v1.0/paths", methods=['GET'])
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


@main.route('/api/v1.0/path/<string:path_id>', methods=['GET'])
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


@main.route("/api/v1.0/article", methods=['POST'])
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


@main.route('/api/v1.0/articles', methods=["GET"])
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


@main.route("/api/v1.0/article/<string:article_id>", methods=['GET'])
def get_article(article_id):
    article = db.articles.find_one({'_id': ObjectId(article_id)})
    article['readtimes'] += 1
    db.articles.update({'_id': article['_id']}, {"$set": {"readtimes": article['readtimes']}})
    article['_id'] = str(article['_id'])
    return jsonify(article)


@main.route('/api/v1.0/folkways', methods=['GET'])
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


@main.route('/api/v1.0/tibet', methods=['GET'])
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


@main.route('/api/v1.0/red_classics', methods=['GET'])
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

