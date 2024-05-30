from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from .models import Usuario
from flask_login import current_user



class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    btn_criar_conta = SubmitField('Criar Conta')

    def validate_email(sellf, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')



class FormLogin(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    btn_login = SubmitField('Login')


    def validade_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError('Esse email, nao está cadastrado, Crie uma conta')
        

class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired()])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    imagem = FileField('Imagem da Post', validators=[FileAllowed(['jpg', 'png', 'jpeg', FileRequired()], 'Apenas arquivos .jpg e .png são permitidos.')])
    btn_criar_post = SubmitField('Publicar')


class EditarPerfilForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Nova Senha', validators=[EqualTo('confirmar_senha', message='As senhas devem coincidir.')])
    confirmar_senha = PasswordField('Confirmar Nova Senha')
    submit = SubmitField('Salvar Alterações')

        # funcao de validacao antes de mudar o email do usuario
    def validate_email(self, email):
        """Essa função é usada para validar se um novo e-mail fornecido em um formulário de registro já está sendo usado por outro usuário. Se um usuário diferente já estiver registrado com o e-mail fornecido, uma mensagem de erro é gerada para informar ao usuário que ele deve fornecer um e-mail único.
        """
        # verificar se o cara mudou o email
        # se o email do usuario atual é diferente do email que ele preencheu
        # Verifica se o e-mail fornecido no formulário de registro é diferente do e-mail atual do usuário logado.
        if current_user.email != email.data:
            # Se o e-mail fornecido é diferente, busca no banco de dados se já existe um usuário com o mesmo e-mail.
            usuario = Usuario.query.filter_by(email=email.data).first()
            # Se um usuário com o mesmo e-mail é encontrado, lança uma exceção de validação com uma mensagem de erro.
            if usuario:
                raise ValidationError('Já existe um usuário com esse E-mail. Por favor, cadastre outro E-mail.')