"""Transactional domain commands. Generic CRUD never writes derived state."""
import uuid
from datetime import date, datetime, timezone
from .repository import Repository
from .db import transaction
from .errors import AppError, Conflict, Forbidden

def rows(conn, name):
    repo = Repository(conn, name)
    return [repo.get(r['id']) for r in conn.execute('SELECT id FROM records WHERE resource=? ORDER BY id', (name,))]

def find(conn, name, **criteria):
    return next((r for r in rows(conn, name) if all((r.get(k) == v for k, v in criteria.items()))), None)

def update(conn, name, row, **changes):
    data = {k: v for k, v in row.items() if k not in ('id', '_version')}
    data.update(changes)
    return Repository(conn, name).update(row['id'], data, row['_version'])

def positive(value, name='quantity'):
    if type(value) is not int or not 0 < value <= 10 ** 12:
        raise AppError(name + ' must be a positive integer')
    return value

def text(value, name):
    if not isinstance(value, str) or not value.strip() or len(value) > 200:
        raise AppError(name + ' must be non-empty text (max 200)')
    return value

def execute(conn, action, data):
    if not isinstance(data, dict):
        raise AppError('JSON object required')
    if action not in ACTIONS:
        raise AppError('Unknown workflow')
    with transaction(conn):
        try:
            return ACTIONS[action](conn, data)
        except KeyError as exc:
            raise AppError('Missing workflow field: ' + str(exc.args[0]))

def consent(conn, patient_id):
    Repository(conn, 'patients').get(patient_id)
    today = date.today().isoformat()
    if not any((r['patient_id'] == patient_id and r['scope'] == 'emergency_card' and (r['status'] == 'granted') and (r['expires_on'] >= today) for r in rows(conn, 'consents'))):
        raise Forbidden('Active emergency card consent is required')

def issue_card(conn, data):
    patient_id = text(data['patient_id'], 'patient_id')
    consent(conn, patient_id)
    existing = find(conn, 'health_cards', patient_id=patient_id, status='active')
    if existing:
        return existing
    return Repository(conn, 'health_cards').create(dict(patient_id=patient_id, card_number='HC-' + uuid.uuid4().hex[:16].upper(), status='active', issued_on=date.today().isoformat()))

def view_card(conn, data):
    card = Repository(conn, 'health_cards').get(text(data['card_id'], 'card_id'))
    if card['status'] != 'active':
        raise Forbidden('Card was revoked')
    consent(conn, card['patient_id'])
    patient = Repository(conn, 'patients').get(card['patient_id'])
    return dict(card_number=card['card_number'], name=patient['name'], blood_group=patient['blood_group'], allergies=[{k: r[k] for k in ('substance', 'reaction', 'severity')} for r in rows(conn, 'allergies') if r['patient_id'] == patient['id']], emergency_contacts=[{k: r[k] for k in ('name', 'relationship', 'phone')} for r in rows(conn, 'emergency_contacts') if r['patient_id'] == patient['id']])

def revoke_card(conn, data):
    card = Repository(conn, 'health_cards').get(text(data['card_id'], 'card_id'))
    return card if card['status'] == 'revoked' else update(conn, 'health_cards', card, status='revoked')

def book_appointment(conn, data):
    patient_id = text(data['patient_id'], 'patient_id')
    provider_id = text(data['provider_id'], 'provider_id')
    starts_at = text(data['starts_at'], 'starts_at')
    try:
        dt = datetime.fromisoformat(starts_at)
        if dt.tzinfo is None:
            raise ValueError()
        normalized = dt.astimezone(timezone.utc).isoformat()
    except ValueError:
        raise AppError('starts_at requires an ISO timestamp with timezone')
    if any((r['provider_id'] == provider_id and r['status'] == 'booked' and (datetime.fromisoformat(r['starts_at']).astimezone(timezone.utc) == dt.astimezone(timezone.utc)) for r in rows(conn, 'appointments'))):
        raise Conflict('Provider slot already booked')
    return Repository(conn, 'appointments').create(dict(patient_id=patient_id, provider_id=provider_id, starts_at=normalized, status='booked', reason=text(data['reason'], 'reason')))

def cancel_appointment(conn, data):
    appointment = Repository(conn, 'appointments').get(text(data['appointment_id'], 'appointment_id'))
    if appointment['status'] == 'completed':
        raise Conflict('Completed appointment cannot be cancelled')
    return update(conn, 'appointments', appointment, status='cancelled')
ACTIONS = {'issue_card': issue_card, 'view_card': view_card, 'revoke_card': revoke_card, 'book_appointment': book_appointment, 'cancel_appointment': cancel_appointment}
