from extension import db
from models import BlockedIP
from app import create_app

app = create_app()

with app.app_context():
    ip_to_unblock = "127.0.0.1"

    blocked = BlockedIP.query.filter_by(ip_address=ip_to_unblock).first()

    if blocked:
        db.session.delete(blocked)
        db.session.commit()
        print(f"✅ IP {ip_to_unblock} unblocked successfully")
    else:
        print(f"⚠️ IP {ip_to_unblock} not found in blocked list")