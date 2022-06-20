import json
from bson import ObjectId
from flask import Flask, session
from celery import Celery
from linkedBot2 import linkedBot_Kamel
from flask import jsonify, request
from flask_pymongo import PyMongo
from linkedBot import linkedBot
import py_eureka_client.eureka_client as eureka_client
from keycloak import KeycloakOpenID
from flask_oidc import OpenIDConnect
from flask_cors import CORS
import nltk
from recommend import recommended
nltk.download("stopwords")
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

port = 5000
eureka_client.init(eureka_server="http://host.docker.internal:8761/eureka",
                   app_name="profils-service",
                   instance_port=port)
app = Flask(__name__)
CORS(app)
app.secret_key = "hello"
app.config['MONGO_URI'] = "mongodb://host.docker.internal:27017/prestalink"
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
mongo = PyMongo(app)

app.config.update({
    'SECRET_KEY': 'TESTING-ANURAG',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_OPENID_REALM': 'prestalink-realm',
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
    'OIDC_TOKEN_TYPE_HINT': 'access_token',
    'OIDC-SCOPES': ['openid']
})

oidc = OpenIDConnect(app)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@celery.task()
def linkedsearch(search):
    link = linkedBot("benpikon@gmail.com", "Motdepasse", mongo)
    # link.browser.quit()
    # passaron.papasarouni@gmail.com/firas.1997/firasghost@gmail.com
    link.login_linkedin()
    link.google_search(search)


@celery.task()
def linkedsearch_kamel(search):
    link = linkedBot_Kamel("benpikon@gmail.com", "Motdepasse", mongo)
    link.login_linkedin()
    linkProfile = link.google_search(search)
    return linkProfile


# @app.route('/login/<user>', methods=["POST", "GET"])
# def login(user):
#     if request.method == "POST":
#         user = request.view_args['user']
#         session["user"] = user
#         return "hello " + user + " u are loged in"


@app.route('/singleScrap/<search>', methods=['POST'])
def scrapping_run_kamel(search):
    if request.method == "POST":
        response = linkedsearch_kamel(search)
        print('in app')
        print(response)
        return response


@app.route('/run/<search>', methods=['POST'])
@oidc.accept_token(require_token=True)
def scrapping_run(search):
    if request.method == "POST":
        response = 'la vie en rose'
        linkedsearch(search)
        return response


@app.route("/<int:page>/<int:number>", methods=['POST'])
def lists(page, number):
    numberProfilePerPage = 8
    ids_profiles_recomended = []
    ids = recommended(request.json['search'], number)
    for id in json.loads(ids).values():
        ids_profiles_recomended.append(ObjectId(id))
    if page >= 1:
        return jsonify([json.loads(JSONEncoder().encode(i)) for i in
                            mongo.db.profiles.find({'_id': {"$in": ids_profiles_recomended}}).skip(
                                (page - 1) * numberProfilePerPage).limit(numberProfilePerPage)])
    else:
        return

    # numberProfilePerPage = 8
    # mongo.db.profiles.create_index([('profile_title', 'text')])
    # keys = request.json['search']
    # print(keys)
    # if page >= 1:
    #     return jsonify([i for i in
    #                     mongo.db.profiles.find({"$text": {"$search": '"\"' + ' '.join((str(n) for n in keys)) + '\""'}},
    #                                            {'_id': False}).sort("match", 1).skip(
    #                         (page - 1) * numberProfilePerPage).limit(numberProfilePerPage)])
    # else:
    #     return


@app.route("/profile", methods=['POST'])
@oidc.accept_token(require_token=True)
def urls():
    link = request.json['link']
    profile = mongo.db.profiles.find_one({'link': link}, {'_id': False})

    return jsonify(profile)


# @app.route('/logout', methods=['POST'])
# def logout():
#     session.pop("user", None)
#     return "good bye"


# @app.route('/recommend/<id>',methods=['POST'])
# def recommend(id):
#     x=recommender(id)
#     return x


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
