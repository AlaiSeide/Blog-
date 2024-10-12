from blog import database, login_manager
from flask_login import UserMixin
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Modelo de Associação para seguidores
followers = database.Table('followers',
    database.Column('follower_id', database.Integer, database.ForeignKey('usuario.id')),
    database.Column('followed_id', database.Integer, database.ForeignKey('usuario.id'))
)

# Modelo de Associação para curtidas
likes = database.Table('likes',
    database.Column('user_id', database.Integer, database.ForeignKey('usuario.id')),
    database.Column('post_id', database.Integer, database.ForeignKey('post.id'))
)

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    senha_hash = database.Column(database.String(120), nullable=False)
    member_since = database.Column(database.DateTime, nullable=False, default=datetime.now(timezone.utc))
    posts = database.relationship('Post', backref='autor', lazy=True)

    followed = database.relationship(
        'Usuario', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=database.backref('followers', lazy='dynamic'), lazy='dynamic'
    )

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return database.session.query(followers).filter(
            followers.c.follower_id == self.id,
            followers.c.followed_id == user.id).count() > 0

    def like_post(self, post):
        if not self.has_liked_post(post):
            post.likes.append(self)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            post.likes.remove(self)

    def has_liked_post(self, post):
        return database.session.query(likes).filter(
            likes.c.user_id == self.id,
            likes.c.post_id == post.id).count() > 0


    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
    
    def __repr__(self):
        return '<Usuario %r>' % self.username

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String(200), nullable=False)
    conteudo = database.Column(database.Text, nullable=False)
    imagem = database.Column(database.String(120), nullable=True)
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    likes = database.relationship('Usuario', secondary=likes, backref=database.backref('liked_posts', lazy='dynamic'))

    def __repr__(self):
        return '<Post %r>' % self.titulo

class Message(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    content = database.Column(database.Text, nullable=False)
    timestamp = database.Column(database.DateTime, index=True, default=datetime.now(timezone.utc))
    sender_id = database.Column(database.Integer, database.ForeignKey('usuario.id'))
    recipient_id = database.Column(database.Integer, database.ForeignKey('usuario.id'))

    sender = database.relationship('Usuario', foreign_keys=[sender_id], backref='sent_messages')
    recipient = database.relationship('Usuario', foreign_keys=[recipient_id], backref='received_messages')
