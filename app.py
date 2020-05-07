#Ariel Chouminov
from flask import Flask, render_template, url_for

app = Flask(__name__)

#create index route
@app.route('/')
def index():
    return render_template('index.html') #knows to look into templates folder to render the html file

if __name__=="__main__":
    app.run(debug=True)