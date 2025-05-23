from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class ArtObject(Base):
    __tablename__ = 'art_object'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    
    painting = relationship("Painting", back_populates="art_object", uselist=False)
    sculpture = relationship("Sculpture", back_populates="art_object", uselist=False)

class Painting(Base):
    __tablename__ = 'painting'
    
    id_painting = Column(Integer, primary_key=True)
    size = Column(Integer)
    type_color = Column(String)
    art_object_id = Column(Integer, ForeignKey('art_object.id', ondelete='CASCADE'))
    
    art_object = relationship("ArtObject", back_populates="painting")

class Sculpture(Base):
    __tablename__ = 'sculpture'
    
    id_sculpture = Column(Integer, primary_key=True)
    weight = Column(Float)
    material = Column(String)
    art_object_id = Column(Integer, ForeignKey('art_object.id', ondelete='CASCADE'))
    
    art_object = relationship("ArtObject", back_populates="sculpture")

engine = create_engine("postgresql://postgres:124512451245@localhost:5432/ooptry3")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
