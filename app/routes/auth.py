from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app.models import User
from app import db

auth = Blueprint('auth', __name__)

# ─────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')
        user     = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('incidents.dashboard'))
        else:
            flash('Email ou mot de passe incorrect', 'danger')

    return render_template('auth/login.html')


# ─────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# ─────────────────────────────────────────
# CREATION DES COMPTES DE DEMO (à appeler une seule fois)
# ─────────────────────────────────────────
@auth.route('/init-demo')
def init_demo():
    if User.query.first():
        return 'Utilisateurs déjà créés.'

    users = [
        {'nom': 'Alice Dupont',  'email': 'declarant@demo.com',   'role': 'declarant',   'mdp': 'demo1234'},
        {'nom': 'Bob Martin',    'email': 'analyste@demo.com',    'role': 'analyste',    'mdp': 'demo1234'},
        {'nom': 'Clara Roux',    'email': 'responsable@demo.com', 'role': 'responsable', 'mdp': 'demo1234'},
        {'nom': 'David Leroy',   'email': 'admin@demo.com',       'role': 'admin',       'mdp': 'demo1234'},
    ]

    for u in users:
        user = User(nom=u['nom'], email=u['email'], role=u['role'])
        user.set_password(u['mdp'])
        db.session.add(user)

    db.session.commit()
    return 'Comptes de démonstration créés avec succès !'
