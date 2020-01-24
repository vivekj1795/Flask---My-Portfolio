from flask import Flask ,render_template,request
from flask_sqlalchemy import SQLAlchemy 
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Comment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

COMMENTS=[]

@app.route('/')
def index():
    return render_template("index1.html")

@app.route('/comment',methods = ['GET','POST'])
def comment():
    comment_list = db.session.query(User).all()[::-1]
    if request.method == "POST":
        name = request.form["name"]
        comment= request.form["comment"]
        obj = User(Name=name,Comment=comment)
        obj = User(Name=name,Comment=comment)
        db.session.add(obj)
        db.session.commit()
        COMMENTS.append((name,comment))
        return render_template("comment.html",COMMENTS=comment_list)
    elif request.method == "GET":
        return render_template("comment.html",COMMENTS=comment_list)
        print(COMMENTS)
        

@app.route('/api/comment')
def commentlist():
    comment_list = db.session.query(User).all()
    comments_list = []
    comment_dict = {}
    for comment in comment_list:
        comment_dict['id']=comment.id
        comment_dict['name']=comment.Name
        comment_dict['comment']=comment.Comment
        comments_list.append(comment_dict)
    return json.dumps(comments_list)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(80),unique=True,nullable=False)
    Comment = db.Column(db.String(120),unique=True,nullable=False)

    def __repr__(self):
        return f"{self.Name} commented {self.comment}"


if __name__ == "__main__":  
    app.run(debug=True)
