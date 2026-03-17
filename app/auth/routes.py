from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from app.models.user import User
from app.auth.forms import LoginForm
from . import auth_bp


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        row = User.get_by_username(form.username.data)
        if row and check_password_hash(row["password"], form.password.data):
            if not row["activo"]:
                flash("Tu cuenta está desactivada.", "danger")
                return render_template("auth/login.html", form=form)
            user = User(row["id"], row["username"], row["activo"])
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.index"))
        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("auth.login"))
