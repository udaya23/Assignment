from flask import Flask, render_template
app = Flask(__name__)      #flask needs to know where to read the files from same direct, name will give the name of the directory that has all other files
from app import app
from db_setup import init_db, db_session
from forms import RecipeSearchForm, RecipeForm
from flask import flash, render_template, request, redirect
from models import Recipe

init_db()
 
 
@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    index() func works with GET and POST requests and loads our RecipeSearchForm.when we first load the index pg of web app,
    it will execute a GET and the index() func will render our index.html
    '''
    search = RecipeSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
 
    return render_template('index.html', form=search)

@app.route('/results')
def search_results(search):
    '''Search_results() func hnadles basic searches'''
    results = []
    search_string = search.data['search']
 
    if search.data['search'] == '':
        qry = db_session.query(Recipe)
        results = qry.all()
 
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', results=results)
 

@app.route('/new_recipe', methods=['GET', 'POST'])
def new_recipe():
    """
    Add a new recipe entry
    """
    form = RecipeForm(request.form)
    return render_template('new_recipe.html', form=form)
 
 
	
if __name__ == '__main__':
    app.run()
    
	
'''	
@app.route('/')
def index():
	 return render_template('index.html')
	 #return "Hello world"

if __name__=='__main__':
	app.run(debug=True)
    '''
	
