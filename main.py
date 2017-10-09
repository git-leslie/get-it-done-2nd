from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done-2nd:root@localhost:8889/get-it-done-2nd'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'                       #for security, will talk about later

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)                   #don't hard delete tasks

    def __init__(self, name):
        self.name = name
        self.completed = False

class User(db.Model):                                   # create model for user class
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)      #email < 120 and no 2 ppl have same email
    password = db.Column(db.String(120))

                                                        #add initializer/constructor for user class
    def __init__(self, email, password):                #users should always have email and password, so those are parameters
        self.email = email
        self.password = password


@app.before_request                                     #run this function before call request handler before upcoming request
def require_login():                                    #not a request handler. this will run every time
    allowed_routes = ['login', 'register']              #list of pages can see w/o being logged in
    if request.endpoint not in allowed_routes and 'email' not in session: #if email key no in session dictionary
        return redirect('/login')                       #redirect to login and force them to login


                                                        # handlers to render the new login and register templates
@app.route('/login', methods=['POST', 'GET'])           #add methods so handler can process requests
def login():
    if request.method == 'POST':                        #check for the request type get-will need to render the form. post-get data out of request and log user in
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first() #verify users password Or else will return special value none
        if user and user.password == password:           #checks if user exists
            session['email'] = email                     # remember" user has logged in
            flash("Logged in")                           #send them a flash message when logged in and put code in base.html
            print(session)
            return redirect('/')                         #when user logs in, redirect to home page. 
        else:                                       #use flash messages instead of error messages
            flash('User password incorrect, or user does not exist', 'error') # TODO tell them why login failed. if don't login, return back to form.
                                                        #error is category string and need to go modify loop in base.thml
            #return '<h1>ERROR!</h1>'                     #for invalid user logins

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':                         #create new user
        email = request.form['email']                    #need email, password, and verify
        password = request.form['password']
        verify = request.form['verify']

        # TODO validate user's data. I HAVE TO DO THIS!!!!!

                                                         #after validate and have a good user, create user from that email and pw
        existing_user = User.query.filter_by(email=email).first() #check if user exists
        if not existing_user:                            #if user doesn't exist
            new_user = User(email, password)             #create new user from info
            db.session.add(new_user)                     #store new user info in db
            db.session.commit()
            session['email'] = email                     #remember the user"
            return redirect('/')
        else:
            #TODO user better response messaging
            return '<h1>Duplicate user</h1>'

    return render_template('register.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':                         #if the incoming request is the form filled out in todos.html
        task_name = request.form['task']                 #then we want to pull the data out and create a new task
        new_task = Task(task_name)                       #create a new task that's a task object
        db.session.add(new_task)                         #put new task in database
        db.session.commit()                              #commit to database NEED TO DO

    #tasks = Task.query.all() #display tasks from the DB (pt2 we added in tasks using Terminal)
    tasks = Task.query.filter_by(completed=False).all()     #before it kept all the tasks, now we want to filter buy ones not completed. Give all the things not completed
    completed_tasks = Task.query.filter_by(completed=True).all() #shows completed tasks below and add to return statement
    return render_template('todos.html',title="Get It Done!", 
        tasks=tasks, completed_tasks=completed_tasks)

@app.route('/delete-task', methods=['POST'])
def delete_tasks():
                                                            #grab the task id and use that to delete from database
    task_id = int(request.form['task-id'])                  #to get a piece of data out of a POST request
                                                            #delete the task with this task id
    task = Task.query.get(task_id)                          #just pull the specific task wtih the specific id
    task.completed = True
    db.session.add(task)                                    #instead of deleting task, like below, put in new column called completed
    db.session.commit()
    
                                                           
                                                            #db.session.delete(task) #flags task object for deletion
                                                            #db.session.commit() #the commit runs the query that actually does the deletion
                                                            
    return redirect('/')                                    #return content from request, redirect to main page

if __name__ == '__main__':
    app.run()