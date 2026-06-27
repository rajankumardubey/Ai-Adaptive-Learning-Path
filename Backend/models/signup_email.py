from sqlalchemy import Column, Integer, String, DateTime, func
from database.connection import Base


class SignupEmail(Base):
    __tablename__ = 'signup_emails'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at,
        }
