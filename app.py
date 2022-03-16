from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initializing the Flask app and Sqlite database
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_DATABSE_URI'] = ' postgresql://jybtlsqpgrgidr:4b0f64f3753a78a8f65532ad706ecb75361b5f325e3f90497f3c8d131ff69cf0@ec2-44-194-167-63.compute-1.amazonaws.com:5432/d527sncsi3d12h'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Creating a database model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(300))
    complete = db.Column(db.Boolean)
    date = db.Column(db.DateTime, nullable= False, default=datetime.utcnow)


@app.route('/')
def home():
    # show all todos
    todo_list = Todo.query.all()

    return render_template('index.html', todo_list=todo_list)


@app.route('/add', methods=['GET', 'POST'])
def add():
    # Add a new task
    title = request.form.get("title")
    description = request.form.get("description")
    new_todo = Todo(title=title, complete=False, description=description)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    # Updating if task completed or not
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # Deleting a task
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    # Creates the Table
    db.create_all()

    app.run(debug=True)
