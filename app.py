from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Save database in the same directory as app.py     
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./task.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    time_created= db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET','POST'])
def home():
    # Add a hardcoded todo item
    if request.method == 'POST':
       title = request.form['title']
       desc = request.form['desc']
       todo = Todo(title=title, desc=desc)
       db.session.add(todo)
       db.session.commit()
   
    all_todo= Todo.query.all()
    return render_template('index.html', all_todo=all_todo)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()

    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect('/')

    return render_template('update.html', todo=todo)



@app.route('/delete/<int:sno>')
def delete(sno):
    todo= Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# Create the tables when the app starts
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
