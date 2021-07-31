"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

class Person():
    def __init__(self, _id, name, last_name, age, parents, children=[]):
        super().__init__()
        self.id = _id
        self.name = name
        self.last_name = last_name
        self.age = age
        self.parents = parents
        self.children = children

ana = Person(1, "Ana", "Garcia Abascal", 89, [], [3,4])
antonio = Person(2, "Antonio", "Melendez Iglesias", 90, [], [3,4])

maria = Person(3, "Maria", "Melendez Garcia", 50, [1,2], [5,6])
raul = Person(4, "Raul", "Melendez Garcia", 55, [1,2], [7,8,9])

lucas = Person(5, "Lucas", "Rivera Melendez", 30, [3])
juan = Person(6, "Juan", "Rivera Melendez", 27, [3])

barbara = Person(7, "Barbara", "Melendez Pacheco", 12, [4])
miriam = Person(8, "Miriam", "Melendez Pacheco", 20, [4])
sofia = Person(9, "Sofia", "Melendez Pacheco", 15, [4])

family = [ana, antonio, maria, raul, lucas, juan, barbara, miriam, sofia]

def get_member(id):
    for person in family:
        if person.id == id:
            return person.__dict__

    return []


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/all', methods=['GET'])
def handle_all():

    fam_sorted = sorted([person.__dict__ for person in family], key=lambda x: x['age'], reverse=True)

    return jsonify(fam_sorted), 200

@app.route('/member/<int:id>', methods=['GET'])
def handle_member_by_id(id):

    member = {}
    parents = []
    children = []

    member = get_member(id)

    if member:

        for parent_id in member['parents']:
            parents.append(get_member(parent_id))

        for children_id in member['children']:
            children.append(get_member(children_id))

        response_body = {
            'member': member,
            'parents': parents,
            'children': children
        }
    
    else:

        response_body = {
            'member': 'Not found'
        }


    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
