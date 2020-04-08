import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


con = 'postgresql://postgres:*@trash-db.cfazlfwlhavj.eu-west-2.rds.amazonaws.com:5432/dbase'

Base = declarative_base()


class Trash(Base):
    __tablename__ = 'trashes'

    id = db.Column(db.Integer, primary_key=True)
    fullness = db.Column('fullness', db.Integer, default=0)
    latitude = db.Column('latitude', db.Float, nullable=False)
    longitude = db.Column('longitude', db.Float, nullable=False)


def get_session():
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def add_trash(lat, long):
    session = get_session()
    trash = Trash(latitude=lat, longitude=long)
    session.add(trash)
    session.commit()
    item = session.query(Trash).filter_by(latitude=lat, longitude=long).one()
    return item.id


def change_trash(value_id, value_fullness):
    session = get_session()
    item = session.query(Trash).filter_by(id=value_id).one()
    item.fullness = value_fullness
    session.add(item)
    session.commit()


def print_all_trash():
    session = get_session()
    for item in session.query(Trash).all():
        print(item.id, item.fullness, item.latitude, item.longitude)


if __name__ == '__main__':
    engine = db.create_engine(con)
    connection = engine.connect()

    # Base.metadata.create_all(engine)  # create table

    # new_id = add_trash(95.234231, 47.231233)
    # print(new_id)

    print_all_trash()
    change_trash(5, 12)
    print_all_trash()






