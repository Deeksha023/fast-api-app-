from sqlalchemy import Column, Integer, String
from database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="Candidate")

    @property
    def name(self):
        return self.username

    @name.setter
    def name(self, value):
        self.username = value