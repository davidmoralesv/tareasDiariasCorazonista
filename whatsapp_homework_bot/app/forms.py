from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Email
from .models import Grade

class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar Sesión')

class SubscriptionForm(FlaskForm):
    """Form for adding a new subscription."""
    whatsapp_number = StringField('Número de WhatsApp', validators=[DataRequired()])
    customer_email = EmailField('Email del Cliente', validators=[DataRequired(), Email()])
    grade = SelectField('Grado', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Crear Suscripción y Generar Enlace de Pago')

    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        # Populate the grade choices dynamically from the database
        self.grade.choices = [(g.id, g.name) for g in Grade.query.order_by('id').all()]
