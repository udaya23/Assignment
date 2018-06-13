from wtforms import Form, StringField, SelectField

"""this class defines all fields required to create a new recipe data entry"""
class RecipeForm(Form):
    Category = [('Breakfast', 'Lunch'),
                   ('Dinner', 'Desserts'),
                   ]
    Recipe_Name = StringField('Recipe Name')
    Link = StringField('Link')

class RecipeSearchForm(Form):
    choices = [('RecipeIndex', 'Name'),
               ('Recipe', 'Recipe_category'),
               ('Recipe', 'Recipename')]
    select = SelectField('Search for recipe:', choices=choices)
    search = StringField('')
	
"""
	Here we just import the items we need from the wtforms module and then we subclass the Form class. In our subclass, we create a selection field (a combobox) and a string field. This allows us to filter our search to the Artist, Album or Publisher categories and enter a string to search for.

Now we are ready to update our main application.
"""