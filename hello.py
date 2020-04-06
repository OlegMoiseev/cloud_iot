from flask import Flask, request, abort, jsonify, render_template
import random
import sqlite3
import work_with_db as dbase


def get_connection():
    conn = sqlite3.connect("trashes.db")  # или :memory: чтобы сохранить в RAM
    return conn, conn.cursor()


app = Flask(__name__,
            static_folder='./static',
            template_folder='./templates')


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
    conn, db = get_connection()
    all_info = dbase.get_all_trash(db)
    if not all_info:
        return "HELO"
    else:
        return str(all_info)


@app.route("/create")
def create():
    conn, db = get_connection()
    dbase.create_table(db, conn)


@app.route("/drop")
def drop():
    conn, db = get_connection()
    dbase.drop_trash(db, conn)


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


@app.route('/add', methods=['POST'])
def add_trash():
    if not request.json or not 'latitude' in request.json or not 'longitude' in request.json:
        abort(400)
    conn, db = get_connection()
    new_id = dbase.add_trash(db, conn, request.json['latitude'], request.json['longitude'])
    return str(new_id), 201


@app.route('/update', methods=['POST'])
def update_trash():
    if not request.json or not 'id' in request.json or not 'fullness' in request.json:
        abort(400)
    conn, db = get_connection()
    print(request.json['id'], request.json['fullness'])
    dbase.change_trash(db, conn, request.json['id'], request.json['fullness'])
    return "UPDATED", 202


if __name__ == "__main__":
    app.run()
