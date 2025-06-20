# USEFUL WHEN ERROR: chrome://net-internals/#sockets

# The most basic flask app you can write
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# initialize database
db = SQLAlchemy(app)

# creating the model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET']) #these methods are required to send data to database
def index(): 
    if request.method == 'POST':
        task_content = request.form['content'] # the contents of the input form
        # create todo object from the todo model
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/') #redirect to index
        except:
            return 'There was an issue adding your task'
    
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() # look at the database in the order of they created
        return render_template('index.html', tasks=tasks)

#need to setup new route for delete
@app.route('/delete/<int:id>') 
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    # try and except is a good practice, if succesful then do the intended operations, if not throw error
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/') # back to homepage
    except:
        return 'There was a problem deleting that task'
    
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)

