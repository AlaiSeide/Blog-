from blog import app, database
from flask import render_template, flash, redirect, url_for, request, abort
from .forms import FormCriarConta, FormLogin, FormCriarPost, EditarPerfilForm, DeleteForm, FormEditPost
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
        email = form.email.data
        senha = form.senha.data
        lembrar_dados = form.lembrar_dados.data

        # buscando um usuario no meu banco de dados que tem esse email, digitado no formulario
        usuario = Usuario.query.filter_by(email=email).first()
        # se existir usuario e se a senha digitada no formulario for igual a senha no meu banco de dados, vou fazer login
        if usuario and usuario.check_senha(senha):
            login_user(usuario, remember=lembrar_dados)
            flash('Login Feito com Sucesso', 'alert-success')
            return redirect(url_for('homepage'))
        else:
            flash('Email ou Senha Incoretos', 'alert-danger')
    return render_template('login.html', form=form)





@app.route('/criarconta', methods=['GET', 'POST'])
def criar_conta():
    form = FormCriarConta()

    if form.validate_on_submit():
        
        # pegando os dados do formulario
        username = form.username.data
        email = form.email.data
        senha = form.senha.data

        usuario = Usuario(username=username, email=email)
        # adicionando a senha no banco de dados mais só que criptografada
        usuario.set_senha(senha)

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
    delete_form = DeleteForm()
    return render_template('detalhes_post.html', post=post, title=post.titulo, delete_form=delete_form)


@app.route('/editarperfil/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
def editar_perfil(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)

    if usuario.id != current_user.id:
        # flash('Você não tem permissão para editar este perfil.', 'alert-danger')
        # return redirect(url_for('homepage'))
        abort(403)
        
    form = EditarPerfilForm()

    if form.validate_on_submit():
        usuario.username = form.username.data
        usuario.email = form.email.data
        # se o usuario digitou uma senha
        if form.senha.data:
            usuario.set_senha(form.senha.data)
        database.session.commit()
        flash('Seu perfil foi atualizado com sucesso!', 'alert-success')
        return redirect(url_for('homepage'))

    # preencher os campos automaticamente
    elif request.method == 'GET':
        form.username.data = usuario.username
        form.email.data = usuario.email

    return render_template('editar_perfil.html', form=form)

@app.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.autor != current_user:
        abort(403)
    form = FormEditPost()
    if form.validate_on_submit():
        post.titulo = form.titulo.data
        post.conteudo = form.descricao.data
        database.session.commit()
        flash('O seu posto foi atualizado!', 'alert-success')
        return redirect(url_for('detalhes_post', post_id=post.id))
    elif request.method == 'GET':
        form.titulo.data = post.titulo
        form.descricao.data = post.conteudo
    return render_template('edit_post.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.autor != current_user:
        abort(403)
    database.session.delete(post)
    database.session.commit()
    flash('A sua Post foi apagada!', 'alert-success')
    return redirect(url_for('homepage'))