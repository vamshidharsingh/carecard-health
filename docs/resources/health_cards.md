# Health Cards

Local card issuance registry; card display rechecks consent each time.

| Field | Type | Constraint |
| --- | --- | --- |
| `patient_id` | string | Reference to `patients` |
| `card_number` | string | Required |
| `status` | string | active, revoked |
| `issued_on` | string | date |

Read endpoint: `GET /api/resources/health_cards`. A local operator bearer token is required.
This resource is read-only through the generic HTTP API. Use the documented business workflows so derived state remains consistent.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `["card_number"]`.
Fixture file: `fixtures/health_cards.json`. Repository exact-match helper: `find_by_patient_id`.
Test module: `tests/test_health_cards.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
