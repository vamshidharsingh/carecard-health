# Access Requests

Manual requests for record-sharing review.

| Field | Type | Constraint |
| --- | --- | --- |
| `patient_id` | string | Reference to `patients` |
| `requester` | string | Required |
| `scope` | string | emergency_card, records |
| `status` | string | pending, approved, denied |

Read endpoint: `GET /api/resources/access_requests`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/access_requests.json`. Repository exact-match helper: `find_by_patient_id`.
Test module: `tests/test_access_requests.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
