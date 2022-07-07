import logging
from contextlib import contextmanager

from dynaconf import settings
from flask import has_app_context
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import exc as sql_exc
from sqlalchemy.orm import scoped_session, sessionmaker


class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(app, options)
        options["pool_pre_ping"] = True
        return options


def get_session():
    global _Session
    if has_app_context():
        _Session = db.session
    if not _Session:
        _create_session_maker()
    return _Session()


def get_engine():
    global _engine
    if not _engine:
        _create_engine()
    return _engine


def pre_ping(session, sample_object=None):
    logger = logging.getLogger(__name__)
    logger.debug('Pre-ping database')
    try:
        if sample_object:
            session.query(sample_object).limit(1).all()
        else:
            session.execute('SELECT 1')
        logger.debug('Ping database success')
        return True
    except (sql_exc.OperationalError, sql_exc.StatementError):
        logger.debug('Retry connection', exc_info=True)
        session.rollback()
        try:
            if sample_object:
                session.query(sample_object).limit(1).all()
            else:
                session.execute('SELECT 1')
        except Exception:
            logger.error('Retried connect to database once and failed, give up', exc_info=True)
            session.rollback()
    except Exception as e:
        session.rollback()
        raise e


def _create_session_maker():
    global _Session
    global _engine
    _Session = sessionmaker()
    if not _engine:
        _create_engine()
    _Session.configure(bind=_engine)
    _Session = scoped_session(_Session)
    return _Session


def _create_engine():
    global _engine
    database_uri = settings.SQLALCHEMY_DATABASE_URI
    _engine = create_engine(database_uri, pool_pre_ping=True, execution_options={})


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = get_session()
    try:
        yield session
    finally:
        session.close()


def is_mysql_session(session):
    return session.bind.dialect.name == 'mysql'


db = SQLAlchemy()
_engine = None
_Session = None
