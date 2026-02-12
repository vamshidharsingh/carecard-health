# Medications

Manual medication record. The app does not prescribe or verify interactions.

| Field | Type | Constraint |
| --- | --- | --- |
| `patient_id` | string | Reference to `patients` |
| `name` | string | Required |
| `dosage` | string | Required |
| `frequency` | string | Required |
| `status` | string | active, stopped |

Read endpoint: `GET /api/resources/medications`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/medications.json`. Repository exact-match helper: `find_by_patient_id`.
Test module: `tests/test_medications.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
