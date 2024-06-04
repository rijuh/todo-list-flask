from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), nullable=True)


@app.route("/", methods=['GET', 'POST'])
def index():
    todos = Todo.query.order_by(Todo.status).all()
    return render_template('index.html', todos=todos)


@app.route("/complete/<int:id>")
def complete(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.status = 'complete'
    db.session.add(todo)
    db.session.commit()
    return redirect('/')


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect('/')


@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    todo = Todo.query.filter_by(id=id).first()
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    return render_template('update.html', todo=todo)


@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

    with app.app_context():
        db.create_all()