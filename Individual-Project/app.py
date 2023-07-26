from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import os

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']



Config = {
  "apiKey": "AIzaSyDwGOo1qGQ651zLFlFIRXJoSfL9WrBBA4s",
  "authDomain": "mini-cs-1.firebaseapp.com",
  "projectId": "mini-cs-1",
  "storageBucket": "mini-cs-1.appspot.com",
  "messagingSenderId": "1004194066679",
  "appId": "1:1004194066679:web:dd0c2e7db8b768869f63f2",
  "measurementId": "G-HSRCTHBS56",
  "databaseURL": "https://mini-cs-1-default-rtdb.europe-west1.firebasedatabase.app/"
};

firebase= pyrebase.initialize_app(Config)
auth= firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS




def upload_file(file):
    if request.method == 'POST':
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(UPLOAD_FOLDER + "/" + filename)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=''
    if request.method == 'POST':
        try:
            email= request.form['email']        
            bio = request.form['bio']           
            username= request.form['usernamee']           
            fullname= request.form['full_name']           
            password = request.form['password']           
            user = {'email':email, 'bio':bio, 'usernamee':username, 'full_name':fullname}
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            db.child('User').child(UID).set(user)
            print('d')
            return redirect(url_for('home'))
        except Exception as e:
            print(e)
            error = 'Authentication failed'
    return render_template("signup.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error=''
    if request.method == 'POST':
        email= request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except Exception as e:
            print(e)
            error = 'Authentication failed'
    return render_template("signin.html")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signout')
def signout():
    login_session['user']= None
    auth.current_user= None
    return redirect(url_for("signin"))

@app.route('/create', methods=['GET', 'POST'])
def add_gossip():
    if request.method == 'POST':
        title1 = request.form['title']
        gossip1 = request.form['gossip']
        img1 = request.files['picture']
        upload_file(img1)
        UID = login_session['user']['localId']
        gossips = {'title':title1, 'gossip':gossip1, 'picture':img1.filename}
        db.child('Gossips').push(gossips)
        return redirect(url_for("home"))
    return render_template("create.html")


@app.route('/home')
def home():

    gossips1 = db.child('Gossips').get().val()
    print(gossips1)
    return render_template("home.html", gossips=gossips1)

@app.route('/profile')
def urprofile():
    UID2 = login_session['user']['localId']
    users1 = db.child('User').child(UID2).get().val()
    return render_template("profile.html", user=users1)


@app.route('/about')
def home2():
    return render_template("home2.html")



#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)