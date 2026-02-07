# Lab Results

Fictional laboratory observations with textual reference ranges.

| Field | Type | Constraint |
| --- | --- | --- |
| `patient_id` | string | Reference to `patients` |
| `test_name` | string | Required |
| `value` | string | Required |
| `unit` | string | Required |
| `reference_range` | string | Required |
| `tested_on` | string | date |

Read endpoint: `GET /api/resources/lab_results`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/lab_results.json`. Repository exact-match helper: `find_by_patient_id`.
Test module: `tests/test_lab_results.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
