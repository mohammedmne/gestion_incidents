from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# ─────────────────────────────────────────
# UTILISATEURS
# ─────────────────────────────────────────
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    nom           = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False)
    mot_de_passe  = db.Column(db.String(200), nullable=False)
    role          = db.Column(db.String(50), nullable=False)
    # roles : declarant / analyste / responsable / admin

    def set_password(self, password):
        self.mot_de_passe = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.mot_de_passe, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ─────────────────────────────────────────
# INCIDENTS
# ─────────────────────────────────────────
class Incident(db.Model):
    __tablename__ = 'incidents'
    id              = db.Column(db.Integer, primary_key=True)
    titre           = db.Column(db.String(200), nullable=False)
    description     = db.Column(db.Text, nullable=False)
    categorie       = db.Column(db.String(100), nullable=False)
    gravite         = db.Column(db.String(50), nullable=False)
    # gravite : faible / moyen / élevé / critique
    statut          = db.Column(db.String(50), default='declaré')
    # statut : declaré / qualifié / en_cours / résolu / clôturé
    date_creation   = db.Column(db.DateTime, default=datetime.utcnow)
    date_cloture    = db.Column(db.DateTime, nullable=True)
    synthese_cloture= db.Column(db.Text, nullable=True)

    declarant_id    = db.Column(db.Integer, db.ForeignKey('users.id'))
    analyste_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    declarant       = db.relationship('User', foreign_keys=[declarant_id])
    analyste        = db.relationship('User', foreign_keys=[analyste_id])
    actions         = db.relationship('Action', backref='incident', lazy=True)


# ─────────────────────────────────────────
# JOURNAL DES ACTIONS
# ─────────────────────────────────────────
class Action(db.Model):
    __tablename__ = 'actions'
    id          = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    auteur_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ancien_statut  = db.Column(db.String(50), nullable=True)
    nouveau_statut = db.Column(db.String(50), nullable=True)
    date        = db.Column(db.DateTime, default=datetime.utcnow)

    auteur      = db.relationship('User', foreign_keys=[auteur_id])
