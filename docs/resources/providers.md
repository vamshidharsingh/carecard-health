# Providers

Fictional healthcare provider directory.

| Field | Type | Constraint |
| --- | --- | --- |
| `name` | string | Required |
| `specialty` | string | Required |
| `registration` | string | Required |

Read endpoint: `GET /api/resources/providers`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `["registration"]`.
Fixture file: `fixtures/providers.json`. Repository exact-match helper: `find_by_name`.
Test module: `tests/test_providers.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
