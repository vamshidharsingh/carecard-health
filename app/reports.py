from .workflows import rows
from .schema import all_schemas
from .repository import Repository

def dashboard(conn):
    counts = {name: Repository(conn, name).count() for name in all_schemas()}
    cards = rows(conn, 'health_cards')
    appointments = rows(conn, 'appointments')
    counts_by_kind = {k: sum((r['kind'] == k for r in rows(conn, 'vitals'))) for k in ('heart_rate', 'temperature', 'systolic_bp')}
    return dict(counts=counts, metrics=[dict(label='Patient profiles', value=counts['patients']), dict(label='Active health cards', value=sum((r['status'] == 'active' for r in cards))), dict(label='Booked appointments', value=sum((r['status'] == 'booked' for r in appointments))), dict(label='Pending access requests', value=sum((r['status'] == 'pending' for r in rows(conn, 'access_requests'))))], bars=[dict(label=k, value=v, target=max(counts_by_kind.values(), default=1) or 1) for k, v in counts_by_kind.items()])
