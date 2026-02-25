# Care Plans

Manual care planning notes; no treatment recommendation engine.

| Field | Type | Constraint |
| --- | --- | --- |
| `patient_id` | string | Reference to `patients` |
| `title` | string | Required |
| `notes` | string | Required |
| `status` | string | active, complete |

Read endpoint: `GET /api/resources/care_plans`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/care_plans.json`. Repository exact-match helper: `find_by_patient_id`.
Test module: `tests/test_care_plans.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
