from configs.connection import DataHandler
from entities.logbook import Logbook

class LbRepo:
    def select(self):
        with DataHandler() as db:
            try:
                data = db.session.query(Logbook).all()
                return data
            except Exception as exception:
                db.session.rollback()
                raise exception
                    
    def insert(self, vbt, vat, aat):
        with DataHandler() as db:
            try:
                data_insert = Logbook(vbt=vbt, vat=vat, aat=aat)
                db.session.add(data_insert)
                db.session.commit()
            except Exception as exception:
                db.session.rollback()
                raise exception
            
    def delete(self, vbt):
        with DataHandler() as db:
            try:
                db.session.query(Logbook).filter(Logbook.vbt == vbt).delete()
                db.session.commit()
            except Exception as exception:
                db.session.rollback()
                raise exception
            
    def update(self, vbt, vat):
        with DataHandler() as db:
            try:
                db.session.query(Logbook).filter(Logbook.vbt == vbt).update({Logbook.vat == vat})
                db.session.commit()
            except Exception as exception:
                db.session.rollback()
                raise exception
