import random
import sqlite3


def create_table(cursor, connection):
    cursor.execute("""CREATE TABLE trashes
                      (id INTEGER PRIMARY KEY, fullness INTEGER DEFAULT 0,
                      latitude REAL, longitude REAL)
                   """)
    connection.commit()


def add_trash(cursor, connection, latitude, longitude):
    cursor.execute('INSERT INTO trashes(latitude, longitude) VALUES(' + str(latitude) + ', ' + str(longitude) + ')')
    connection.commit()
    cursor.execute('SELECT id FROM trashes WHERE latitude=' + str(latitude) + ' AND longitude=' + str(longitude))
    return cursor.fetchone()[0]


def drop_trash(cursor, connection):
    cursor.execute('DROP TABLE trashes')
    connection.commit()


def change_trash(cursor, connection, id, fullness):
    cursor.execute('UPDATE trashes SET fullness=' + str(fullness) + ' WHERE id=' + str(id))
    connection.commit()


def print_all_trash(cursor):
    cursor.execute('SELECT * FROM trashes')

    rows = cursor.fetchall()
    for row in rows:
        print(row)


def get_all_trash(cursor):
    cursor.execute('SELECT * FROM trashes')
    return cursor.fetchall()


def get_one_trash(cursor, id):
    cursor.execute('SELECT * FROM trashes WHERE id=' + str(id))
    return cursor.fetchone()


if __name__=='__main__':
    conn = sqlite3.connect("trashes.db")  # или :memory: чтобы сохранить в RAM
    db = conn.cursor()

    latitude = round(random.uniform(-90, 90), 6)
    longitude = round(random.uniform(-180, 180), 6)

    # new_id = add_trash(db, conn, latitude, longitude)
    # print(new_id)
    # change_trash(db, conn, 1, 45)
    # print(get_all_trash(db))
    drop_trash(db, conn)
    create_table(db, conn)
