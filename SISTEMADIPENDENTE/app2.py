from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from flask import send_from_directory
import os 
import pyodbc
from MSSQLConn import conn

#Creazione di app e cartelle per l'ambiente di progetto

app = Flask(__name__)
app.secret_key="Marco"

#archiviazione foto di definizione

FOLDER = os.path.join('uploads')
app.config['FOLDER']=FOLDER

@app.route('/uploads/<nomeFoto>') #percorso in cui sono archiviate le foto
def uploads(nomeFoto):
    return send_from_directory(app.config['FOLDER'],nomeFoto)

#---------------------------------------------------------------------------------------------------

#La pagina iniziale dell'applicazione carica le informazioni della pagina dei dipendenti

@app.route('/')
def index():

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM dipendenti;")
            dipendenti = cursor.fetchall()
            for dipendente in dipendenti:
                print(dipendente)

    except Exception as e:
        print("Si è verificato un errore: ", e)
    
    return render_template('dipendenti/index.html', dipendenti=dipendenti)

#funzione per avviare la pagina di creazione del dipendente

@app.route('/create')
def create():

    return render_template('dipendenti/create.html')

#funzione per acquisire le informazioni fornite nel modello creato, quindi viene inserito nel database

@app.route('/store', methods = ['POST'])
def storage():
    
    _nome=request.form['txtNome']
    _cognome=request.form['txtCognome']
    _mail=request.form['txtMail']
    _dipartimento=request.form['txtDipartimento']
    _foto=request.files['txtFoto']

    if _nome=='' or _cognome=='' or _mail=='' or _dipartimento=='' or _foto=='':
        flash('Ricordati di compilare i dati nei campi')
        return redirect(url_for('create'))

    now = datetime.now()
    tempo = now.strftime("%Y%M%D%H%S")

    if _foto.filename != '':
        nuovoNomeFoto = tempo + _foto.filename
        nuovoNomeFoto = nuovoNomeFoto.replace('/','')
        _foto.save( "uploads/" + nuovoNomeFoto )

    dati = ( _nome, _cognome, _mail, _dipartimento, nuovoNomeFoto )

    try:
        with conn.cursor() as cursor:

            sql = "INSERT INTO dipendenti ( NOME, COGNOME, MAIL, DIPARTIMENTO, FOTO) VALUES ( ?, ?, ?, ?, ? )"
            cursor.execute(sql, dati)
            conn.commit()

    except Exception as e:

        print("Si è verificato un errore : ", e)

    return redirect('/')

#funzione per modificare il dipendente, caricare prima le informazioni del dipendente selezionato

@app.route('/edit/<int:id>')
def edit(id):

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM dipendenti WHERE id = ?;", (id) )
            dipendenti = cursor.fetchall()
            for dipendente in dipendenti:
                print(dipendente)

    except Exception as e:
        print("Si è verificato un errore : ", e)

    return render_template('dipendenti/edit.html', dipendenti=dipendenti)

#funzione per aggiornare i dati del dipendente secondo i dati modificati nella maschera EDIT

@app.route('/update', methods = ['POST'])
def update():
    
    _nome=request.form['txtNome']
    _cognome=request.form['txtCognome']
    _mail=request.form['txtMail']
    _dipartimento=request.form['txtDipartimento']
    _foto=request.files['txtFoto']
    _id=request.form['txtID']

    dati = ( _nome, _cognome, _mail, _dipartimento, _id )

    try:
        with conn.cursor() as cursor:

            sql = "UPDATE dipendenti SET nome = ?, cognome = ?, mail = ?, dipartimento = ? WHERE id = ?;"
            now = datetime.now()
            tempo = now.strftime("%Y%M%D%H%S")    

            if _foto.filename != '':
                nuovoNomeFoto = tempo + _foto.filename
                nuovoNomeFoto = nuovoNomeFoto.replace('/','')
                _foto.save( "uploads/" + nuovoNomeFoto )
                cursor.execute("SELECT FOTO FROM dipendenti WHERE id = ?;", _id)
                riga=cursor.fetchall()
                os.remove(os.path.join(app.config['FOLDER'],riga[0][0]))
                cursor.execute("UPDATE dipendenti SET FOTO = ? WHERE id = ?;", (nuovoNomeFoto, _id))
                conn.commit()
    
            cursor.execute(sql, dati)
            conn.commit()

    except Exception as e:
        print("Si è verificato un errore : ", e)

    return redirect('/')


#funzione per eliminare il record esistente del dipendente nel database. riceve le informazioni attraverso il form INDEX.html

@app.route('/destroy/<int:id>')
def destroy(id):

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT FOTO FROM dipendenti WHERE id = ?;", id)
            riga=cursor.fetchall()
            os.remove(os.path.join(app.config['FOLDER'],riga[0][0]))
            cursor.execute( "DELETE FROM dipendenti WHERE id=?", (id) )
            conn.commit()

    except Exception as e:
        print("Si è verificato un errore : ", e)
    
    return redirect('/')

#creare il server per eseguire l'applicazione corrispondente

if __name__== '__main__':
    app.run(debug=True)