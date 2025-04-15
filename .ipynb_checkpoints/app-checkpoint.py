from playertrack.stats import allstat
from flask import Flask, render_template, request, flash, redirect, send_file, url_for,session,get_flashed_messages
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app = Flask(__name__, static_folder='assets')
app.secret_key="emna"

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='gark'

mysql =MySQL(app)

# ***************** requette home ***************************
@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html',username=session['username'])
    else:
        return render_template("index.html")
        
# ***************** requette de logout ***************************
@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))


# ***************** requette de login ***************************

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=="POST":
        email=request.form["email"]
        pwd=request.form['pwd']

        if not all([email,pwd]):
            flash('Veuillez remplir les champs.', 'vide')
        else :
            cur=mysql.connection.cursor()
            cur.execute(f"select username, email , pwd from user where email='{email}'")
            User=cur.fetchone()
            cur.close()
            if User and pwd == User[2]:
                session['username']=User[0]
                return redirect(url_for('home'))
            
            else :
                flash('Email ou mot de passe invalide.', 'error')

        messages=get_flashed_messages(with_categories=True)
        return render_template('login.html',messages=messages)

    return render_template('login.html')

# ***************** requette de signup ***************************

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userid = request.form['userid'].replace(" ", "")
        username =request.form['username']
        email = request.form['email']
        phone = request.form['phone'].replace(" ", "")
        pwd = request.form['pwd']
        # pwd2 = request.form['pwd']

        # if not all([userid,username,email,phone,pwd,pwd2]):
        #     flash('Veuillez remplir tous les champs requis.', 'error')

# verifé existence de l'utilisateur 
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE email=%s OR userid=%s", (email, userid))
        existe = cur.fetchone()
        cur.close()

        if existe:
            flash('Email ou numéro d\'identité déja utiliser.', 'error')
#  nouveau utilisateur -> insertion dans la base           
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user (userid, username, email, phone, pwd) VALUES (%s, %s, %s, %s, %s)", (userid, username, email, phone, pwd))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('login'))
        
    messages=get_flashed_messages(with_categories=True)
    return render_template('signup.html',messages=messages)




@app.route('/up')
def up():
    return render_template('uplode.html',username=session['username'])

# ***************** requette d'uplode vidéo ***************************

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'mp4','MOV','WEBM'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uplode', methods=['GET', 'POST'])
def uplode():
    if request.method == 'POST':
        # if 'file' not in request.files:
        #     flash('No file part', 'error')
        #     return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Aucun fichier sélectionné', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            source_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            target_filename = filename.rsplit('.', 1)[0] + '_output.mp4'
            target_path = os.path.join(app.config['OUTPUT_FOLDER'], target_filename)
            # Appel à la fonction all() avec les deux chemins de fichier
            tracked_player_detections = allstat(source_path, target_path)
            session['tracked_player_detections'] = tracked_player_detections
            # Retourner le fichier cible en téléchargement
            return redirect(url_for('report'))
        
        flash('Format fichier non pris en charge.', 'error')

    messages = get_flashed_messages(with_categories=True)
    return render_template('uplode.html', messages=messages)

@app.route('/report')
def report():
    tracked_player_detections = session.get('tracked_player_detections', [])
    # Utilisation des données dans votre template ou logique de vue
    return render_template('report.html', tracked_player_detections=tracked_player_detections ,username=session['username'])

if __name__ == '__main__':
     app.run(debug=True) 