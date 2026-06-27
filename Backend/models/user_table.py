from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, func
from database.connection import Base


class UserTable(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    mobile = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    learning_level = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'learning_level': self.learning_level,
            'created_at': self.created_at,
            'mobile': self.mobile,
        }
