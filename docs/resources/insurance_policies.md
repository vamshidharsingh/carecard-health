# Insurance Policies

Masked policy metadata without insurance verification.

| Field | Type | Constraint |
| --- | --- | --- |
| `patient_id` | string | Reference to `patients` |
| `provider` | string | Required |
| `policy_reference` | string | Required |
| `expires_on` | string | date |

Read endpoint: `GET /api/resources/insurance_policies`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/insurance_policies.json`. Repository exact-match helper: `find_by_patient_id`.
Test module: `tests/test_insurance_policies.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
