from app import db


class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def save(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(pk):
        raise NotImplementedError
