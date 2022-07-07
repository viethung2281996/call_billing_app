
from . import db, models


CALL_BLOCK_DURATION_SEC = 30


def get_or_create_user(user_name):
    user_db = db.session.query(models.User).filter(models.User.user_name == user_name).first()
    if not user_db:
        user_db = models.User(user_name=user_name)
        db.session.add(user_db)
        db.session.commit()
    return user_db


def add_call_billing(user_id, call_duration):
    call_db = models.CallBilling(user_id=user_id, call_duration=call_duration)
    call_db.block_count = _caculate_call_block_count(call_db.call_duration)
    db.session.add(call_db)
    db.session.commit()
    return call_db


def _caculate_call_block_count(call_duration):
    call_duration_sec = int(call_duration / 1000)
    if call_duration_sec % CALL_BLOCK_DURATION_SEC == 0:
        return int(call_duration_sec / CALL_BLOCK_DURATION_SEC)
    else:
        return int(call_duration_sec / CALL_BLOCK_DURATION_SEC) + 1
