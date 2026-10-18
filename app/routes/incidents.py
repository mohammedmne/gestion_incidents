from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from app.models import Incident, Action, User
from app import db
from datetime import datetime

incidents = Blueprint('incidents', __name__)

@incidents.route('/')
@incidents.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'declarant':
        liste = Incident.query.filter_by(declarant_id=current_user.id).all()
    else:
        liste = Incident.query.order_by(Incident.date_creation.desc()).all()

    stats = {
        'total'    : Incident.query.count(),
        'critique' : Incident.query.filter_by(gravite='critique').count(),
        'en_cours' : Incident.query.filter_by(statut='en_cours').count(),
        'clotures' : Incident.query.filter_by(statut='clôturé').count(),
    }
    return render_template('incidents/dashboard.html', incidents=liste, stats=stats)


@incidents.route('/incident/nouveau', methods=['GET', 'POST'])
@login_required
def nouveau():
    if request.method == 'POST':
        incident = Incident(
            titre        = request.form.get('titre'),
            description  = request.form.get('description'),
            categorie    = request.form.get('categorie'),
            gravite      = request.form.get('gravite'),
            statut       = 'declaré',
            declarant_id = current_user.id
        )
        db.session.add(incident)
        db.session.flush()

        action = Action(
            incident_id    = incident.id,
            auteur_id      = current_user.id,
            description    = 'Incident déclaré',
            ancien_statut  = None,
            nouveau_statut = 'declaré'
        )
        db.session.add(action)
        db.session.commit()
        flash('Incident déclaré avec succès.', 'success')
        return redirect(url_for('incidents.dashboard'))

    return render_template('incidents/nouveau.html')


@incidents.route('/incident/<int:id>')
@login_required
def detail(id):
    incident  = Incident.query.get_or_404(id)
    analystes = User.query.filter_by(role='analyste').all()
    return render_template('incidents/detail.html', incident=incident, analystes=analystes)


@incidents.route('/incident/<int:id>/statut', methods=['POST'])
@login_required
def changer_statut(id):
    incident = Incident.query.get_or_404(id)
    nouveau  = request.form.get('nouveau_statut')
    note     = request.form.get('note', '')
    ancien   = incident.statut
    incident.statut = nouveau

    if nouveau == 'clôturé':
        incident.date_cloture     = datetime.utcnow()
        incident.synthese_cloture = request.form.get('synthese', '')

    action = Action(
        incident_id    = incident.id,
        auteur_id      = current_user.id,
        description    = note or f'Statut changé vers {nouveau}',
        ancien_statut  = ancien,
        nouveau_statut = nouveau
    )
    db.session.add(action)
    db.session.commit()
    flash(f'Statut mis à jour : {nouveau}', 'success')
    return redirect(url_for('incidents.detail', id=id))


@incidents.route('/incident/<int:id>/affecter', methods=['POST'])
@login_required
def affecter(id):
    incident    = Incident.query.get_or_404(id)
    analyste_id = request.form.get('analyste_id')
    incident.analyste_id = analyste_id
    analyste = User.query.get(analyste_id)

    action = Action(
        incident_id    = incident.id,
        auteur_id      = current_user.id,
        description    = f'Incident affecté à {analyste.nom}',
        ancien_statut  = incident.statut,
        nouveau_statut = incident.statut
    )
    db.session.add(action)
    db.session.commit()
    flash('Analyste affecté avec succès.', 'success')
    return redirect(url_for('incidents.detail', id=id))


@incidents.route('/incident/<int:id>/action', methods=['POST'])
@login_required
def ajouter_action(id):
    incident    = Incident.query.get_or_404(id)
    description = request.form.get('description')

    action = Action(
        incident_id    = incident.id,
        auteur_id      = current_user.id,
        description    = description,
        ancien_statut  = incident.statut,
        nouveau_statut = incident.statut
    )
    db.session.add(action)
    db.session.commit()
    flash('Action ajoutée au journal.', 'success')
    return redirect(url_for('incidents.detail', id=id))


@incidents.route('/api/alerte', methods=['POST'])
def recevoir_alerte():
    data = request.get_json()

    incident = Incident(
        titre        = data.get('titre', 'Alerte IDS'),
        description  = data.get('description', 'Détecté automatiquement'),
        categorie    = data.get('categorie', 'Intrusion réseau'),
        gravite      = data.get('gravite', 'élevé'),
        statut       = 'declaré',
        declarant_id = 1
    )
    db.session.add(incident)
    db.session.flush()

    action = Action(
        incident_id    = incident.id,
        auteur_id      = 1,
        description    = f"Incident créé automatiquement par IDS — Source : {data.get('ip_source', 'inconnue')}",
        ancien_statut  = None,
        nouveau_statut = 'declaré'
    )
    db.session.add(action)
    db.session.commit()

    return jsonify({'status': 'ok', 'incident_id': incident.id}), 201