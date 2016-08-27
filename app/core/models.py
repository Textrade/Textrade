from app import db


class BaseModel:
    def create(self):
        db.session.commit(self)
        return self
