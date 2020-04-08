from flask import Flask, request, abort, jsonify, render_template
import random
import sqlite3
import work_with_db as dbase
from flask_sqlalchemy import SQLAlchemy
from os import environ


def get_connection():
    conn = sqlite3.connect("trashes.db")  # или :memory: чтобы сохранить в RAM
    return conn, conn.cursor()


app = Flask(__name__,
            static_folder='./static',
            template_folder='./templates')

login = environ['MASTER_USER']
password = environ['MASTER_KEY']


url = 'postgresql://' + str(login) + ':' + str(password) + '@trash-db.cfazlfwlhavj.eu-west-2.rds' \
                                        '.amazonaws.com:5432/dbase'

app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Trash(db.Model):
    __tablename__ = 'trashes'

    id = db.Column(db.Integer, primary_key=True)
    fullness = db.Column('fullness', db.Integer, default=0)
    latitude = db.Column('latitude', db.Float, nullable=False)
    longitude = db.Column('longitude', db.Float, nullable=False)


@app.route("/")
def root():
    return render_template('dashboard.html')


@app.route("/dashboard.html")
def dash():
    return render_template('dashboard.html')


@app.route("/map.html")
def map():
    return render_template('map.html')


@app.route("/graph.html")
def graph():
    return render_template('graph.html')


@app.route("/get_all")
def get_all():
    all_info = '['
    for item in Trash.query.all():
        all_info += '(' + str(item.id) + ', ' + str(item.fullness) + ', ' + str(item.latitude) + ', '\
                    + str(item.longitude) + '), '
    all_info = all_info[:-2] + ']'

    if not all_info:
        return "HELO"
    else:
        return all_info


@app.route('/add', methods=['POST'])
def add_trash():
    if not request.json or not 'latitude' in request.json or not 'longitude' in request.json:
        abort(400)

    lat = request.json['latitude']
    long = request.json['longitude']
    trash = Trash(latitude=lat, longitude=long)
    db.session.add(trash)
    db.session.commit()
    new_item = Trash.query.filter_by(latitude=lat, longitude=long).one()
    return str(new_item.id), 201


@app.route('/update', methods=['POST'])
def update_trash():
    if not request.json or not 'id' in request.json or not 'fullness' in request.json:
        abort(400)
    item = Trash.query.filter_by(id=request.json['id']).one()
    item.fullness = request.json['fullness']
    db.session.commit()
    return "UPDATED", 202


@app.route('/create')
def create():
    db.create_all()
    return "CREATED", 201


@app.route('/drop')
def drop():
    db.drop_all()
    return "DROPPED", 200

# ----------------------------------------------------------
@app.route('/trash/<int:trash_id>', methods=['GET'])
def get_trash(trash_id):
    conn, db = get_connection()
    info = dbase.get_one_trash(db, trash_id)
    if info is not None:
        return jsonify({'ID': info[0],
                        'Fullness': info[1],
                        'Latitude': info[2],
                        'Longitude': info[3]
                        })
    else:
        abort(404)


@app.route("/add_random")
def add_random():
    conn, db = get_connection()
    latitude = round(random.uniform(-90, 90), 6)
    longitude = round(random.uniform(-180, 180), 6)
    new_id = dbase.add_trash(db, conn, latitude, longitude)
    return str(new_id)




if __name__ == "__main__":
    app.run()
