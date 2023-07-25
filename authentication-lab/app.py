from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

firebaseConfig = {
  "apiKey": "AIzaSyC7OMSS9KH_eHNCpJPMrZA4sbN5Yzd_Ii8",
  "authDomain": "medlen-87694.firebaseapp.com",
  "projectId": "medlen-87694",
  "storageBucket": "medlen-87694.appspot.com",
  "messagingSenderId": "423031549738",
  "appId": "1:423031549738:web:8e0fbe42bad14a5c6bb853",
  "measurementId": "G-Z04TQFQENY","databaseURL":"https://medlen-87694-default-rtdb.europe-west1.firebasedatabase.app/"
};

firebase =pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username=request.form['username']
        fullname=request.form['fullname']
        bio=request.form['bio']
        
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID=login_session['user']['localId']
            usern={'un':username,'fl':fullname,'bio':bio}
            db.child("Users").child(UID).set(usern)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
            return render_template("signin.html")
    return render_template("signup.html")

@app.route('/', methods=['GET', 'POST'])
def signin():

   
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password =request.form['password']
       try:
         login_session['user'] = auth.sign_in_with_email_and_password(email, password)
         return redirect(url_for('add_tweet'))
       except:
        error = "Authentication failed"
   return render_template("signin.html", error=error)


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))




@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():

    return render_template("add_tweet.html")

@app.route('/all_tweets', methods=['GET', 'POST'])
def see_tweet():
    if request.method == 'POST':
        tweet={ "text": request.form['ttext'], "title": request.form['ttitle'], "uid":login_session['user']['localId']}
        db.child("Tweets").push(tweet)
        return render_template("all_tweets.html",title=db.child("Tweets").get().val())
        return render_template("add_tweet.html")



    
if __name__ == '__main__':
    app.run(debug=True)




ghghghg