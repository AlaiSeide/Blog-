from blog import app, database
from flask import render_template, flash, redirect, url_for, request
from .forms import FormCriarConta, FormLogin, FormCriarPost, EditarPerfilForm
from flask_login import login_user, logout_user, current_user, login_required
from .models import Usuario, Post
from werkzeug.utils import secure_filename
import os

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
        login_user(usuario, remember=True)
        flash('Conta Criar Com Successo', 'alert-success')
        return redirect(url_for('homepage'))
    return render_template('register.html', form=form)



@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com Successo', 'alert-info')
    return redirect(url_for('homepage'))

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')


@app.route('/criarpost', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()

    if form.validate_on_submit():
        imagem = form.imagem.data
        nome_seguro = secure_filename(imagem.filename)
        # os.path.abspath(os.path.dirname(__file__)) caminho do meu projeto onde está o routes.py
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nome_seguro)
         # Salvando a imagem na pasta static/imagens
        imagem.save(caminho)
        # Criando o novo post
        post = Post(titulo=form.titulo.data, conteudo=form.descricao.data, imagem=nome_seguro, usuario_id=current_user.id)
        database.session.add(post)
        database.session.commit()

        flash('Seu post foi criado com sucesso!', 'alert-success')
        return redirect(url_for('homepage'))

    return render_template('create_post.html', form=form)


@app.route('/detalhes/<post_id>')
def detalhes_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('detalhes_post.html', post=post)


@app.route('/editarperfil/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
def editar_perfil(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)

    if usuario.id != current_user.id:
        flash('Você não tem permissão para editar este perfil.', 'alert-danger')
        return redirect(url_for('home'))

    form = EditarPerfilForm()

    if form.validate_on_submit():
        usuario.username = form.username.data
        usuario.email = form.email.data
        if form.senha.data:
            usuario.set_senha(form.senha.data)
        database.session.commit()
        flash('Seu perfil foi atualizado com sucesso!', 'alert-success')
        return redirect(url_for('homepage'))

    elif request.method == 'GET':
        form.username.data = usuario.username
        form.email.data = usuario.email

    return render_template('editar_perfil.html', form=form)