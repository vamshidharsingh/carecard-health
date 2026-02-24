"""Immunization history entered by the demo operator."""
from app.repository import Repository

class ResourceRepository(Repository):
    resource = 'vaccinations'

    def find_by_patient_id(self, value):
        """Return exact matches, independent of the paginated UI listing."""
        rows = self.conn.execute('SELECT id FROM records WHERE resource=? ORDER BY id', (self.resource,))
        return [item for row in rows if (item := self.get(row['id']))['patient_id'] == value]
