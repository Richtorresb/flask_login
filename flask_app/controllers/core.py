import os

from flask import redirect, render_template, request, flash, session
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():

    if 'email' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')

    nombre_sistema = "Coding Dojo"  
    return render_template("index.html", sistema=nombre_sistema)

@app.route("/login")
def login():

    if 'email' in session:
        flash('Ya estás LOGEADO!', 'warning')
        return redirect('/')

    return render_template("login.html")

@app.route("/procesar_registro", methods=["POST"])
def procesar_registro():

    if not Usuario.validar(request.form):
        return redirect('/login')

    pass_hash = bcrypt.generate_password_hash(request.form['pasword'])

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'pasword' : pass_hash,
    }

    resultado = Usuario.save(data)

    if not resultado:
        flash("error al crear el usuario", "error")
        return redirect("/login")

    flash("Usuario creado correctamente", "success")
    return redirect("/login")


@app.route("/procesar_login", methods=["POST"])
def procesar_login():

    usuario = Usuario.buscar(request.form['identificacion'])
    print(usuario)

    if not usuario:
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    if not bcrypt.check_password_hash(usuario.pasword, request.form['pasword']):
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    session['email'] = usuario.email
    session['first_name'] = usuario.first_name

    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')