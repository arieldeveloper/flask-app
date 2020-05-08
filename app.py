#Ariel Chouminov
from flask import Flask, render_template, url_for, request, redirect
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
@app.route('/', methods=['POST', 'GET']) #We can now send data to database with post
def index():
    if request.method == "POST":
        task_content = request.form["content"] #refers to id in the html template
        #If content is empty give an alert
        if task_content == "":
            tasks = Todo.query.order_by(Todo.date_created).all()
            return render_template("index.html", tasks=tasks, error=True)
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error when adding a task" #error message
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() #Shows the entire database by date created
        return render_template('index.html', tasks=tasks, error=False) #knows to look into templates folder to render the html file

@app.route('/delete/<int:id>')
def delete(id):
    taskToDelete = Todo.query.get_or_404(id)
    try:
        db.session.delete(taskToDelete)
        db.session.commit()
        return redirect('/') #refreshes the page
    except:
        return "There was an issue deleting your task"

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content'] #setting the tasks content to the forms value given
        if task.content == "":
            return render_template("update.html", task=task, error=True)
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating your task"
    else:
        return render_template('update.html', task=task, error=False)

if __name__=="__main__":
    app.run(debug=True) #debug on for development