from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done-2nd:root@localhost:8889/get-it-done-2nd'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean) #don't hard delete tasks

    def __init__(self, name):
        self.name = name
        self.completed = False


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST': #if the incoming request is the form filled out in todos.html
        task_name = request.form['task'] #then we want to pull the data out and create a new task
        new_task = Task(task_name) #create a new task that's a task object
        db.session.add(new_task) #put new task in database
        db.session.commit() #commit to database NEED TO DO

    #tasks = Task.query.all() #display tasks from the DB (pt2 we added in tasks using Terminal)
    tasks = Task.query.filter_by(completed=False).all() #before it kept all the tasks, now we want to filter buy ones not completed. Give all the things not completed
    completed_tasks = Task.query.filter_by(completed=True).all() #shows completed tasks below and add to return statement
    return render_template('todos.html',title="Get It Done!", 
        tasks=tasks, completed_tasks=completed_tasks)

@app.route('/delete-task', methods=['POST'])
def delete_tasks():
    #grab the task id and use that to delete from database
    task_id = int(request.form['task-id']) #to get a piece of data out of a POST request
    #delete the task with this task id
    task = Task.query.get(task_id) #just pull the specific task wtih the specific id
    task.completed = True
    db.session.add(task) #instead of deleting task, like below, put in new column called completed
    db.session.commit()
    
    '''
    db.session.delete(task) #flags task object for deletion
    db.session.commit() #the commit runs the query that actually does the deletion
    '''
    #return content from request, redirect to main page
    return redirect('/')

if __name__ == '__main__':
    app.run()