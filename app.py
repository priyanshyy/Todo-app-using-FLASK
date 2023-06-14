from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy #to make databases in flask
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///Todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

# is database ko create krne k liye:
#     1. terminal m python likho and enter
#     2. type-> from app(project name) import app,db
#     3. app.app_context().push()
#     4. db.create_all()
#     5. exit()
# Todo.db bnn jaega

    #jb bhi iss object ko print kre to ky dikhega vo hum "repr" m likhengy
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


#app route
@app.route('/', methods=['GET','POST'])
def hello_world():
    #when push submit button on form, this will happen
    if request.method=='POST':
        titlee=request.form['title']
        descc=request.form['desc']
        #what to do when we land on our first page
        todo = Todo(title=titlee,desc=descc)
        db.session.add(todo) #to add an entry in db
        db.session.commit()  #to commit changes

    allTodo = Todo.query.all()
    return render_template('index.html',allTodo=allTodo)  #render_template hi pages (templates m saved h jo) run krega using return statement

#another page 
@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is a products page'

#update page
@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        titlee=request.form['title']
        descc=request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title=titlee
        todo.desc=descc
        db.session.add(todo) 
        db.session.commit() 
        return redirect('/')
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
    

#delete page
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True) #,port=8000 to change the port 