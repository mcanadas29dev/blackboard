from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        "Usuario",
        validators=[
            DataRequired(message="El usuario es obligatorio."),
            Length(min=3, max=64, message="Entre 3 y 64 caracteres."),
        ],
    )
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(message="La contraseña es obligatoria.")],
    )
    submit = SubmitField("Entrar")
