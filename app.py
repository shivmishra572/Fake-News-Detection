# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 23:53:33 2021

@author: SHIVAM MISHRA
"""

import pickle
from flask import Flask,render_template,url_for,request,redirect
import mysql.connector


# load the model from disk
filename = 'nlp_model.pkl'
clf = pickle.load(open(filename, 'rb'))
cv=pickle.load(open('tranform.pkl','rb'))
app = Flask(__name__)

#Creating connection to database

conn = mysql.connector.connect(host="remotemysql.com", user="xlD37v65ft", password="Txbd1LQckn", database="xlD37v65ft")
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('loginpage.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/webpage')
def webpage():
	return render_template('webpage2.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get("email")
    password = request.form.get("password")

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'"""
    .format(email,password))
    users = cursor.fetchall()

    if len(users)>0:
        return redirect('/webpage')
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    return redirect('/')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    
    cursor.execute("""INSERT INTO `users` (`user_id`,`name`,`email`,`password`) VALUES (NULL,'{}','{}','{}')""".format(name,email,password))

    conn.commit()
    return redirect('/login')


@app.route('/predict', methods=['POST'])
def predict():
    
    if request.method == 'POST':
        message = request.form['message']
        data = [message]
        vect = cv.transform(data).toarray()
        my_prediction = clf.predict(vect)
    return render_template('webpage2.html',prediction = my_prediction)


if __name__ == '__main__':
	app.run(debug=True)