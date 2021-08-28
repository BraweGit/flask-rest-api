from db import db

class BaseModel(db.Model):
    # __abstract__ -> Model/Table won't be created in the DB.
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)