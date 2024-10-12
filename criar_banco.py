from blog import app, database

from blog.models import Usuario, Post, Message


with app.app_context():
    database.drop_all()
    database.create_all()