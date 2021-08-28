from .base import BaseModel
from db import db

class ItemModel(BaseModel):
    __tablename__ = 'item'
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def json(self):
        return {'name': self.name, 'description': self.description}

    def __repr__(self) -> str:
        return f'Name: {self.name}, Description: {self.description}'

