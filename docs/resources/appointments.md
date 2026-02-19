# Appointments

Provider reservations with exact-slot conflict protection.

| Field | Type | Constraint |
| --- | --- | --- |
| `patient_id` | string | Reference to `patients` |
| `provider_id` | string | Reference to `providers` |
| `starts_at` | string | datetime |
| `status` | string | booked, cancelled, completed |
| `reason` | string | Required |

Read endpoint: `GET /api/resources/appointments`. A local operator bearer token is required.
This resource is read-only through the generic HTTP API. Use the documented business workflows so derived state remains consistent.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/appointments.json`. Repository exact-match helper: `find_by_patient_id`.
Test module: `tests/test_appointments.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
