from blog import app, database

from blog.models import Usuario, Post


with app.app_context():
    database.drop_all()
    database.create_all()