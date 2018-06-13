from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///myrecipes.db', echo=True)
Base = declarative_base()
 
 
class RecipeCategory(Base):
    __tablename__ = "RecipeCategory"
 
    #id = Column(Integer, primary_key=True)
    id = Column(Integer)
    name = Column(String, primary_key=True)
 
    def __repr__(self):
        return "{}".format(self.name)
 
 
class Recipe(Base):
    """"""
    __tablename__ = "Recipes"
 
    id = Column(Integer, primary_key=True)
    #title = Column(String)
    Link = Column(String)
    Recipe_Name = Column(String)
    #media_type = Column(String)
 
    Recipe_category = Column(String, ForeignKey("RecipeCategory.name"))
    Recipename = relationship("RecipeCategory", backref=backref(
        "Recipes"))
 
# create tables
Base.metadata.create_all(engine)