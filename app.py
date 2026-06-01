from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f'<Task {self.id}>'


with app.app_context():
    db.create_all()    


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST': 
        task_content = request.form['content'] 
        db.session.add(ToDo(content=task_content)) 
        db.session.commit() 
        return redirect('/') 
    tasks = ToDo.query.order_by(ToDo.date_created).all() 
    return render_template('app/index.html', tasks=tasks)


@app.route('/delete/<int:id>')   
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit() 
    except:
        return 'couldn`t delete data'    
    
    
@app.route('/update/<int:id>')   
def update(id):
    task = ToDo.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect('/')
 

if __name__ == "__main__":
    app.run(debug=True)