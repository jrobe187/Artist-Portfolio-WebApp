
from flask import Flask, render_template, request, flash, redirect, url_for, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
from models import db, post, users, about
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy, model
import sqlalchemy
import boto3
from gmail import send_email

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

s3 = boto3.resource('s3')

## DATABASE IMPLEMENTATION 
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@localhost:5432/{db_name}'

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return db.session.get(users, int(id))


######HOME######
@app.route('/')
def home():
    
    return render_template('home.html')


######LOGIN######
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Retrieve info from login form
        username = request.form.get('username')
        password = request.form.get('password')

        #Query database to find user with matching email
        user = users.query.filter_by(username=username).first()
        

        if user:
            if user.pw == password:
                flash('user logged in')
                login_user(user)
                return redirect(url_for('gallery'))
        
        # If the login was unsuccessful, reload the login page with an error message
        flash("Invalid Login")
    
     # Render the login page template for GET requests
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return render_template('home.html')

######GALLERY######
@app.route('/post', methods=['GET', 'POST'])
def post(): 
    pass

@app.route('/gallery/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        user_id = 1
        id = 1
        url = 'null'
        title = request.form.get('title')
        body = request.form.get('body')

        post = post(id=id, url=url, title=title, body=body, user_id=user_id)
        db.session.add(post)




@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    
  
    return render_template('gallery.html')



@app.route('/gallery/view_post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post =  post.query.get(post_id)
    return render_template('view_post.html', post=post)


######ABOUT######
@app.route('/about_me', methods=['GET', 'POST'])
def about_me():
    if request.method == 'POST':
        return render_template('edit_am.html')
    user_id = 1
    result = about.query.filter_by(user_id=user_id).first()

    if result:
        text = result.body
    else:
        text = 'Nothing Found'
    


    return render_template('about_me.html', text=text)

@app.route('/about_me/edit_am', methods=['GET', 'POST'])
@login_required
def edit_am():
    if request.method == 'POST':
        print('swag')
        body = request.form['about_me']
        
        user_id = current_user.id 
        result = about.query.filter_by(user_id=user_id).first()

        if result:
            result.body = body
            db.session.commit()
            print("redirecting to about_me")
            
        else:
            new_entry = about(user_id=user_id, body=body)
            db.session.add(new_entry)
            db.session.commit()
        return redirect(url_for('about_me'))
             
        
    
    return render_template('edit_am.html')

    

       


######CONTACT######
@app.route('/contact_me', methods=['GET', 'POST'])
def contact_me():
    if request.method == 'POST':
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        email = request.form['email']
        body = request.form['message']
        

        name = f_name + " " + l_name

        send_email(email=email, body=body, name=name)

    return render_template('contact_me.html')



if __name__ == '__main__':
    app.run(debug=True)





