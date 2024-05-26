from blog import app, database
from flask import render_template, flash, redirect, url_for
from .forms import FormCriarConta, FormLogin
from flask_login import login_user, logout_user, current_user, login_required
from .models import Usuario, Post


@app.route('/')
def homepage():
    # ordenar os post do recentes para mais antigos order_by(Post.id.desc())
    posts = Post.query.order_by(Post.id.desc())
    return render_template('homepage.html', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()

    if form.validate_on_submit():

        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario:
            login_user(usuario)
            flash('Login Feito com Sucesso', 'alert-success')
            return redirect(url_for('homepage'))
        else:
            flash('Email ou Senha Incoretos', 'alert-danger')
    return render_template('login.html', form=form)


@app.route('/criarconta', methods=['GET', 'POST'])
def criar_conta():
    form = FormCriarConta()

    if form.validate_on_submit():
        usuario = Usuario(username=form.username.data, email=form.email.data, senha=form.senha.data)
        database.session.add(usuario)
        database.session.commit()
        flash('Conta Criar Com Successo', 'alert-success')
        return redirect(url_for('homepage'))
    return render_template('register.html', form=form)
