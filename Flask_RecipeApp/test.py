
from flask import Flask, render_template
app = Flask(__name__)      #flask needs to know where to read the files from same direct, name will give the name of the directory that has all other files
from app import app
from db_setup import init_db

init_db()
 
 
@app.route('/')
def test():
    return "Welcome to Flask!"
 
if __name__ == '__main__':
    app.run()
    
