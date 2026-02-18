from app.workflows import execute, rows, update
from app.repository import Repository
from app.errors import AppError, Conflict, Forbidden, NotFound
from tests.helpers import DatabaseCase

class WorkflowTests(DatabaseCase):

    def issue(self):
        return execute(self.conn, 'issue_card', dict(patient_id='patient-1'))

    def test_issue_requires_active_consent(self):
        row = Repository(self.conn, 'consents').get('consent-1')
        update(self.conn, 'consents', row, status='revoked')
        with self.assertRaises(Forbidden):
            self.issue()

    def test_expired_consent_rejected(self):
        row = Repository(self.conn, 'consents').get('consent-1')
        update(self.conn, 'consents', row, expires_on='2000-01-01')
        with self.assertRaises(Forbidden):
            self.issue()

    def test_card_issue_is_repeatable(self):
        self.assertEqual(self.issue()['id'], self.issue()['id'])

    def test_emergency_summary_minimizes_data(self):
        card = self.issue()
        summary = execute(self.conn, 'view_card', dict(card_id=card['id']))
        self.assertNotIn('date_of_birth', summary)
        self.assertNotIn('lab_results', summary)
        self.assertIn('emergency_contacts', summary)

    def test_revoked_consent_blocks_existing_card(self):
        card = self.issue()
        row = Repository(self.conn, 'consents').get('consent-1')
        update(self.conn, 'consents', row, status='revoked')
        with self.assertRaises(Forbidden):
            execute(self.conn, 'view_card', dict(card_id=card['id']))

    def test_revoked_card_is_blocked(self):
        card = self.issue()
        execute(self.conn, 'revoke_card', dict(card_id=card['id']))
        with self.assertRaises(Forbidden):
            execute(self.conn, 'view_card', dict(card_id=card['id']))

    def appointment(self, time='2027-01-01T09:00:00+00:00'):
        return execute(self.conn, 'book_appointment', dict(patient_id='patient-1', provider_id='provider-1', starts_at=time, reason='Demo visit'))

    def test_slot_conflict_across_timezone_offsets(self):
        self.appointment()
        with self.assertRaises(Conflict):
            self.appointment('2027-01-01T14:30:00+05:30')

    def test_naive_appointment_rejected(self):
        with self.assertRaises(AppError):
            self.appointment('2027-01-01T09:00:00')

    def test_cancel_releases_exact_slot(self):
        row = self.appointment()
        execute(self.conn, 'cancel_appointment', dict(appointment_id=row['id']))
        self.assertEqual(self.appointment()['status'], 'booked')

    def test_unknown_patient_rolls_back(self):
        with self.assertRaises(NotFound):
            execute(self.conn, 'issue_card', dict(patient_id='missing'))
        self.assertEqual(rows(self.conn, 'health_cards'), [])
