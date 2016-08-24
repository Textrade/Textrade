from app import db


class BaseModel(db.Model):
    def create(self):
        db.session.commit(self)
        return self
