# Emergency Contacts

Contacts included in consented emergency card summaries.

| Field | Type | Constraint |
| --- | --- | --- |
| `patient_id` | string | Reference to `patients` |
| `name` | string | Required |
| `relationship` | string | Required |
| `phone` | string | Required |

Read endpoint: `GET /api/resources/emergency_contacts`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/emergency_contacts.json`. Repository exact-match helper: `find_by_patient_id`.
Test module: `tests/test_emergency_contacts.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
