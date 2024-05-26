from blog import database, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuario.get(user_id)

class Usuario(database.Model, UserMixin):

    # unique=True: Garante que todos os valores nessa coluna sejam únicos.
    # nullable=False: Garante que a coluna não pode ter valores nulos (é obrigatória).

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    senha = database.Column(database.String(120), nullable=False)

    posts = database.relationship('Post', backref='autor', lazy=True)

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
