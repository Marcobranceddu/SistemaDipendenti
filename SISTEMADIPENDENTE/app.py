from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
import os 

app = Flask(__name__)
app.secret_key="Marco"

FOLDER = os.path.join('uploads')
app.config['FOLDER']=FOLDER

@app.route('/uploads/<nomeFoto>')
def uploads(nomeFoto):
    return send_from_directory(app.config['FOLDER'],nomeFoto)



#MySQL Connection-----------------------------------------------------------------------------------

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3307
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Mitate9907'
app.config['MYSQL_DATABASE_DB'] = 'sistema'
mysql.init_app(app)

#---------------------------------------------------------------------------------------------------

@app.route('/')
def index():

    sql = "SELECT * FROM sistema.dipendenti;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    dipendenti = cursor.fetchall()
    print(dipendenti) 

    conn.commit()
    
    return render_template('dipendenti/index.html', dipendenti=dipendenti)

@app.route('/create')
def create():

    return render_template('dipendenti/create.html')

@app.route('/store', methods = ['POST'])
def storage():
    
    _nome=request.form['txtNome']
    _cognome=request.form['txtCognome']
    _mail=request.form['txtMail']
    _foto=request.files['txtFoto']

    if _nome=='' or _cognome=='' or _mail=='' or _foto=='':
        flash('Ricordati di compilare i dati nei campi')
        return redirect(url_for('create'))

    now = datetime.now()
    tempo = now.strftime("%Y%M%D%H%S")

    if _foto.filename != '':
        nuovoNomeFoto = tempo + _foto.filename
        nuovoNomeFoto = nuovoNomeFoto.replace('/','')
        _foto.save( "uploads/" + nuovoNomeFoto )

    dati = ( _nome, _cognome, _mail, nuovoNomeFoto )

    sql = "INSERT INTO dipendenti VALUES ( NULL, %s, %s, %s, %s )"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, dati)
    conn.commit()

    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute( "SELECT * FROM sistema.dipendenti WHERE id=%s", (id) )
    dipendenti = cursor.fetchall()    
    conn.commit()
    print(dipendenti)

    return render_template('dipendenti/edit.html', dipendenti=dipendenti)

@app.route('/update', methods = ['POST'])
def update():
    
    _nome=request.form['txtNome']
    _cognome=request.form['txtCognome']
    _mail=request.form['txtMail']
    _foto=request.files['txtFoto']
    _id=request.form['txtID']

    dati = ( _nome, _cognome, _mail, _id )

    sql = "UPDATE sistema.dipendenti SET nome = %s, cognome = %s, mail = %s WHERE id = %s;"
    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()
    tempo = now.strftime("%Y%M%D%H%S")

    if _foto.filename != '':
        nuovoNomeFoto = tempo + _foto.filename
        nuovoNomeFoto = nuovoNomeFoto.replace('/','')
        _foto.save( "uploads/" + nuovoNomeFoto )
        cursor.execute("SELECT FOTO FROM sistema.dipendenti WHERE id = %s;", _id)
        riga=cursor.fetchall()
        os.remove(os.path.join(app.config['FOLDER'],riga[0][0]))
        cursor.execute("UPDATE sistema.dipendenti SET FOTO = %s WHERE id = %s;", (nuovoNomeFoto, _id))
        conn.commit()
    
    cursor.execute(sql, dati)
    conn.commit()

    return redirect('/')

@app.route('/destroy/<int:id>')
def destroy(id):

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT FOTO FROM sistema.dipendenti WHERE id = %s;", id)
    riga=cursor.fetchall()
    os.remove(os.path.join(app.config['FOLDER'],riga[0][0]))
    cursor.execute( "DELETE FROM sistema.dipendenti WHERE id=%s", (id) )
    conn.commit()
    
    return redirect('/')

if __name__== '__main__':
    app.run(debug=True)