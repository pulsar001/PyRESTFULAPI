#!/usr/bin/python3

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
import uuid

db_connect = create_engine('sqlite:///parrainages.db')

conn = db_connect.connect()
query = conn.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='utilisateurs' ''')
if query.fetchone()[0]==0 : {
    conn.execute('''CREATE TABLE utilisateurs (id_user varchar(255), unites int(255))''')
}

app = Flask(__name__)
api = Api(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


class AjouterUtilisateur(Resource):
    def get(self):
        conn = db_connect.connect()
        id_user = str(uuid.uuid4())
        query = conn.execute("insert into utilisateurs (id_user, unites) values (?, ?)", (id_user, int(0)))
        return {'id_user': id_user, 'unites': 0} # Donne une ID unique par utilisateur et la stock dans la bdd

class VoirUtilisateurs(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select id_user, unites from utilisateurs")
        result = {'donnees': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class VoirUtilisateurID(Resource):
    def get(self, id_user):
        conn = db_connect.connect()
        query = conn.execute("select id_user, unites from utilisateurs where id_user = ? ", (id_user))
        result = {'donnees': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class ModifierUnites(Resource):
    def get(self, id_user, typing):
        conn = db_connect.connect()
        if typing == "plus": sqlType = "unites = unites + 1"
        else: sqlType = "unites = unites - 1" 
        query = conn.execute("update utilisateurs set " + sqlType + " where id_user = ? ", (id_user))
        query = conn.execute("select id_user, unites from utilisateurs where id_user = ? ", (id_user))
        result = {'donnees': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Defaut(Resource):
    def get(self):
        info = '''Aucun argument'''
        return info

api.add_resource(Defaut, '/')
api.add_resource(AjouterUtilisateur, '/AjouterUtilisateur')
api.add_resource(VoirUtilisateurs, '/VoirUtilisateurs')
api.add_resource(VoirUtilisateurID, '/VoirUtilisateurID/<id_user>')
api.add_resource(ModifierUnites, '/ModifierUnites/<id_user>/<typing>')


if __name__ == '__main__':
     app.run(port='8008')