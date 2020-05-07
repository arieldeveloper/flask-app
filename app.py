#Ariel Chouminov
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db' #set
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False) #Don't let user to leave this empty
    date_created = db.Column(db.DateTime, default=datetime.utcnow) #will automatically be set to the time

    def __repr__(self):
        return '<Task %r>' % self.id #every time a task is created it will return the id

#create index route
@app.route('/')
def index():
    return render_template('index.html') #knows to look into templates folder to render the html file

if __name__=="__main__":
    app.run(debug=True)