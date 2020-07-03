from flask import Flask,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime

with open('config.json','r') as c:
    Prameters = json.load(c)["Prameters"]

local_server=True
app=Flask(__name__)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = Prameters['gmail'],
    MAIL_PASSWORD= Prameters['pass']
)
mail = Mail(app)

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = Prameters['local_uri']
    db=SQLAlchemy(app)
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = Prameters['prod_uri']
    db = SQLAlchemy(app)

class Contacts(db.Model):
    c_id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(80), nullable=False)
    c_email = db.Column(db.String(80), nullable=False)
    c_phone_no = db.Column(db.String(80), nullable=False)
    c_message = db.Column(db.String(80), nullable=False)
    c_date = db.Column(db.String(80), nullable=True)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(30), nullable=False)
    tag_line = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(80), nullable=True)


@app.route("/")
def index():
    posts = Posts.query.filter_by().all()[0:Prameters['no_of_posts']]
    return render_template('index.html', Prameters=Prameters, posts=posts)


@app.route('/post/<string:post_slug>', methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',Prameters=Prameters,post=post)


@app.route('/about')
def about():
    return render_template('about.html',Prameters=Prameters)


@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
    if ('u_name' in session and session['u_name']=='sourabh'):
        return render_template('login.html',Prameters=Prameters)



    if request.method=='POST':
        username= request.form.get('uname')
        password= request.form.get('pass')
        if(username=="sourabh"and password==12345):
            session['u_name']=username
            return render_template('dashboard.html',Prameters=Prameters)


    else:
        return render_template('login.html',Prameters=Prameters)

# @app.route('/post')
# def post():
#     return render_template('post.html',Prameters=Prameters)

@app.route('/contact',methods=['GET','POST'])
def contact():
    if(request.method == 'POST'):
        name = request.form.get('c_name')
        email = request.form.get('c_email')
        phone = request.form.get('c_phone_no')
        msg = request.form.get('c_message')
        entry = Contacts(c_name = name,c_email=email,c_phone_no=phone,c_message=msg,c_date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients=['sourabhrathoresr2@gmail.com'],
                          body='email is :'+ email + "\n" +'Phone is :'+ phone + "\n" + 'Massage is :' + msg
                          )
    return render_template('contact.html',Prameters=Prameters)

if __name__=="__main__":
    app.run(debug=True)
