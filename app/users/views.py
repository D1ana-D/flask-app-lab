from flask import render_template, request, url_for, redirect, flash, session, make_response
from datetime import datetime, timedelta
from . import user_bp

USER_DATA = {
    "username": "user1",
    "password": "123"
}

@user_bp.route("/hi/<string:name>")
def greetings(name):
    name_upper = name.upper()
    age = request.args.get("age", None, type=int)
    return render_template("users/hi.html", name=name_upper, age=age)

@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    return redirect(to_url)

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USER_DATA["username"] and password == USER_DATA["password"]:
            session["user"] = username
            flash("Успішний вхід у систему!", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Wrong data! Try again!", "error")
            return redirect(url_for("users.login"))

    return render_template("users/login.html")

@user_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Ви успішно вийшли з системи.", "info")
    return redirect(url_for("users.login"))

@user_bp.route("/profile", methods=["GET"])
def profile():
    if "user" not in session:
        flash("Будь ласка, увійдіть для доступу до профілю!", "error")
        return redirect(url_for("users.login"))

    username = session["user"]
    cookies = request.cookies
    theme = cookies.get("theme", "light")

    return render_template("users/profile.html", username=username, cookies=cookies, theme=theme)

# Додавання cookie
@user_bp.route("/cookie/add", methods=["POST"])
def add_cookie():
    if "user" not in session:
        return redirect(url_for("users.login"))

    key = request.form.get("key")
    value = request.form.get("value")
    max_age = request.form.get("max_age", type=int)

    response = make_response(redirect(url_for("users.profile")))
    if key and value:
        if max_age and max_age > 0:
            response.set_cookie(key, value, max_age=max_age)
        else:
            response.set_cookie(key, value)
        flash(f"Кукі '{key}' успішно додано!", "success")
    else:
        flash("Будь ласка, вкажіть ключ та значення кукі!", "error")

    return response

@user_bp.route("/cookie/delete", methods=["POST"])
def delete_cookie():
    if "user" not in session:
        return redirect(url_for("users.login"))

    key = request.form.get("key")
    response = make_response(redirect(url_for("users.profile")))
    if key:
        if key in request.cookies:
            response.delete_cookie(key)
            flash(f"Кукі '{key}' успішно видалено!", "info")
        else:
            flash(f"Кукі з ключем '{key}' не знайдено!", "error")
    return response

@user_bp.route("/cookie/delete_all", methods=["POST"])
def delete_all_cookies():
    if "user" not in session:
        return redirect(url_for("users.login"))

    response = make_response(redirect(url_for("users.profile")))
    for key in request.cookies:
        response.delete_cookie(key)
    flash("Усі кукі успішно видалено!", "info")
    return response

@user_bp.route("/change_theme/<string:theme_name>")
def change_theme(theme_name):
    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie("theme", theme_name, max_age=30*24*60*60)
    flash(f"Кольорову схему змінено на {theme_name}!", "success")
    return response