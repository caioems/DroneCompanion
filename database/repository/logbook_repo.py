from configs.connection import DataHandler
from entities.logbook import Logbook

class LbRepo:
    def select(self):
        with DataHandler() as db:
            data = db.session.query(Logbook).all()
            return data