# Vitals

Manually recorded observations without automated clinical interpretation.

| Field | Type | Constraint |
| --- | --- | --- |
| `patient_id` | string | Reference to `patients` |
| `kind` | string | heart_rate, temperature, systolic_bp |
| `value` | number | Required |
| `unit` | string | Required |
| `recorded_at` | string | datetime |

Read endpoint: `GET /api/resources/vitals`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/vitals.json`. Repository exact-match helper: `find_by_patient_id`.
Test module: `tests/test_vitals.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
