from blog import database, login_manager
from flask_login import UserMixin
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(database.Model, UserMixin):

    # unique=True: Garante que todos os valores nessa coluna sejam únicos.
    # nullable=False: Garante que a coluna não pode ter valores nulos (é obrigatória).

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    senha_hash = database.Column(database.String(120), nullable=False)
    member_since = database.Column(database.DateTime, nullable=False, default=datetime.now(timezone.utc))
    posts = database.relationship('Post', backref='autor', lazy=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    # o parametro senha seria a senha do formulario, e self.senha_hash seria a senha criptografada que está no meu banco de dados
    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
    
    def __repr__(self):
        return '<Usuario %r>' % self.username

    # precisamos adicionar a tabela Post com uma coluna que funciona como uma chave estrangeira, apontando para a chave primária da tabela Usuario. Isso estabelece um relacionamento entre as duas tabelas, onde um usuário pode ter múltiplos posts, mas cada post pertence a um único usuário.

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String(200), nullable=False)
    conteudo = database.Column(database.Text, nullable=False)
    imagem = database.Column(database.String(120), nullable=True)  # Coluna para armazenar o nome do arquivo da imagem
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.titulo
