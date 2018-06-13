from app import db
 
 
class RecipeIndex(db.Model):
    __tablename__ = "RecipeCategory"
 
    id = db.Column(db.Integer)
    name = db.Column(db.String, primary_key=True)
 
    def __repr__(self):
        return "<RecipeCategory: {}>".format(self.name)
 
 
class Recipe(db.Model):
    """"""
    __tablename__ = "Recipes"
 
    id = db.Column(db.Integer, primary_key=True)
    #title = db.Column(db.String)
    Link = db.Column(db.String)
    #release_date = db.Column(db.String)
    #publisher = db.Column(db.String)
    #media_type = db.Column(db.String)
 
    Recipe_category = db.Column(db.String, db.ForeignKey("RecipeCategory.name"))
    Recipename = db.relationship("RecipeCategory", backref=db.backref(
        "Recipes"), lazy=True)