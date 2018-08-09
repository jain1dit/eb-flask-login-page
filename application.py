from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_session import Session
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///tutorial.db', echo=True)
 
application = Flask(__name__)
application.config['SESSION_TYPE'] = 'filesystem'
application.secret_key = os.urandom(24)
sess = Session()


@application.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('logout.html')
        
@application.route('/Population', methods=['POST'])
def show_pop():
	Session = sessionmaker(bind=engine)
	sp = Session()
	return render_template('population.html', Popula = sp.query(Population).all() )
 
@application.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@application.route("/logout")
def logout():
    session['logged_in'] = False
    return home()
 
if __name__ == "__main__":
    sess.init_app(application)
    application.run(debug=True)