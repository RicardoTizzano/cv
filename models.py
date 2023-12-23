import db
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime

class Contacto(db.Base):
    __tablename__ = "contacto"
    id_contacto = Column(Integer, primary_key=True, autoincrement=True)
    name    = Column(String, nullable=False)
    email     = Column(String, nullable=False)
    date     = Column(Date, default=datetime.utcnow)
    message   = Column(String)

    def __init__(self, name, email, date, message):
        self.name  = name
        self.email   = email
        self.date   = date
        self.message = message
