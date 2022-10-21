from configs.connection import DataHandler
from entities.logbook import Logbook

class LbRepo:
    def select(self):
        with DataHandler() as db:
            data = db.session.query(Logbook).all()
            return data
        
    def insert(self, vbt, vat, aat):
        with DataHandler() as db:
            data_insert = Logbook(vbt=vbt, vat=vat, aat=aat)
            db.session.add(data_insert)
            db.session.commit()
            
        