from sqlalchemy.orm import DeclarativeBase, Relationship
from sqlalchemy import Column, Integer, String, Float

class Base(DeclarativeBase):
    pass

class ToDo(Base):
    __tablename__ = "to_do"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)
    percentage = Column(Float)

if __name__ == "__main__":
    from sqlalchemy import create_engine
    import os
    from dotenv import load_dotenv
    load_dotenv()

    DATABASE_URL = os.environ.get('DATABASE_URL')
    engine = create_engine(DATABASE_URL, echo=True)

    Base.metadata.create_all(bind=engine)