from models import ActivityLog
from extension import db
from flask import has_app_context, has_request_context, request
from flask_login import current_user

def log_activity(action):
    if not has_app_context():
        return

    user_id = None
    ip_address = None

    if has_request_context():
        ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
        if ip_address and "," in ip_address:
            ip_address = ip_address.split(",")[0].strip()

        if current_user.is_authenticated:
            user_id = current_user.id

    log = ActivityLog(
        user_id=user_id,
        action=action,
        ip_address=ip_address
    )

    try:
        db.session.add(log)
        db.session.commit()
    except Exception:
        db.session.rollback()
