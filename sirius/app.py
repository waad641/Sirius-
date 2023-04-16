#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from passlib.hash import sha256_crypt
#from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
from sqlhelpers import *
from forms import *

#from database import mysql, session
import time

#import mysql.connector
import mysql 


#from passwords import _mysql_password
app = Flask(__name__)

app.secret_key='123'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = 'waad'
app.config['MYSQL_DB'] = 'crypto'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #accessing information by dictionnairy

mysql= MySQL(app)


def log_in_user(username):
    users = Table("users", "name", "email", "username", "password")
    user = users.getone("username", username)

    session['logged_in'] = True
    session['username'] = username
    session['name'] = user.get('name')
    session['email'] = user.get('email')

    

   
@app.route("/register", methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    users=Table("users","name","email","username","password")
    
    if request.method == 'POST' and form.validate() :
        username = form.username.data
        name = form.name.data
        email = form.email.data

        if isnewuser(username) : #check if new user
            password = sha256_crypt.encrypt(form.password.data)
            users.insert(name,email,username,password)
            log_in_user(username)
            return redirect(url_for('dashboard'))
        else:
            flash('user already exist','danger')
            return redirect(url_for('register')) 


    return render_template('register.html',form=form)




@app.route("/login", methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        candidate = request.form['password']

        users = Table("users", "name", "email", "username", "password")
        user = users.getone("username", username)
        accpass = user.get('password')
        
        if accpass is None:
            flash('username is not found','danger')
            return redirect(url_for('login'))
        else :
            if sha256_crypt.verify(candidate, accpass):
                log_in_user(username)  
                flash("you are now logged in.",'success') 
                return redirect(url_for('dashboard'))
            else :
                flash("Invalid password ",'danger')
                return redirect(url_for('login'))     
    return render_template('login.html')



@app.route("/logout")
#@is_logged_in
def logout():
    session.clear()
    flash("Logout  success",'success')
    return redirect(url_for('login')) 




@app.route("/transaction", methods = ['GET', 'POST'])
#@is_logged_in
def transaction():
    form = SendMoneyForm(request.form)
    balance = get_balance(session.get('username'))

    #if form is submitted
    if request.method == 'POST':
        try:
            #attempt to execute the transaction
            send_money(session.get('username'), form.username.data, form.amount.data)
            flash("Money Sent!", "success")
        except Exception as e:
            flash(str(e), 'danger')

        return redirect(url_for('transaction'))
    
    return render_template('transaction.html', balance=balance, form=form, page='transaction')

@app.route("/buy", methods=['GET','POST'])
def buy():
    form = BuyForm(request.form)
    balance = get_balance(session.get('username'))


    if request.method == 'POST': 
        try:
            send_money("BANK", session.get('username'), form.amount.data)
            flash("Purchase Successfull","success")
        except Exception as e:
            flash(str(e),'danger')

        return redirect(url_for('dashboard')) 
    return render_template('buy.html', balance=balance, form=form, page='buy')           




@app.route("/dashboard", methods = ['GET', 'POST'])
#@is_logged_in
def dashboard():
    blockchain = get_blockchain().chain
    ct= time.strftime("%I:%M %p")
   
   
 
    return render_template('dashboard.html', session=session, ct=ct, blockchain=blockchain ,page='dashboard')   


@app.route("/")  
@app.route("/index")          
def index():
    #send_money("BANK", "rawdha", 600)
    


  
    #test_blockchain()
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run(debug = True)





