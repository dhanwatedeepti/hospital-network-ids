from models import ActivityLog
from extension import db
from flask_login import current_user

def log_activity(action):

    try:
        if current_user and current_user.is_authenticated:
            log = ActivityLog(
                user_id=current_user.id,
                action=action
            )
            db.session.add(log)
            db.session.commit()
    except:
        # fallback for scripts / no user context
        log = ActivityLog(
            user_id=None,
            action=action
        )
        db.session.add(log)
        db.session.commit()