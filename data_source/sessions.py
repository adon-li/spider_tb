

from data_source.engines import get_engine
from db_setting import DATA_SOURCE
from sqlalchemy.orm import sessionmaker, scoped_session


def sessions_scopes(_sessions):
    scopes = {}
    for key, _session in _sessions.items():
        scopes.update({key: scoped_session(_session)})
    return scopes


sessions = {}

for source in DATA_SOURCE.keys():
    sessions.update({source: sessionmaker(bind=get_engine(DATA_SOURCE[source]))})
