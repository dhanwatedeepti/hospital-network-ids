from flask import Blueprint, render_template, redirect
from flask import url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user 
from models import User, Patient, Alert
from flask_login import login_required
from flask import jsonify
from models import BlockedIP
from flask import current_app
from utils import log_activity
from models import ActivityLog
from datetime import datetime, timedelta
from models import Alert, BlockedIP
# from sqlalchemy import func
from extension import db


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@login_required
def admin_home():
    
    if current_user.role != "admin":
        return "Access Denied", 403

    
    
    # 📈 Attacks over time (last 7 entries for simplicity)
    recent_attacks = Alert.query.order_by(Alert.timestamp.desc()).limit(7).all()

    users = User.query.all()
    patients = Patient.query.all() #passing all patients
    alerts = Alert.query.order_by(Alert.timestamp.desc()).limit(10).all()
    
    logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(5).all()

    blocked_ips = BlockedIP.query.all()
    blocked_count = len(blocked_ips)
    # log_activity("Created new user")

    return render_template(
        "dashboard_admin.html",
        users=users,
        patients=patients,
        alerts=alerts,
        logs=logs, 
        total_users=User.query.count(),
        total_patients=Patient.query.count(),
        total_attacks=Alert.query.count(),
        blocked_ips=blocked_ips,
        blocked_count=blocked_count
        # blocked_ips=BlockedIP.query.count.all()
        
    )
    
@admin_bp.route('/alerts')
@login_required
def get_alerts():
    from models import Alert

    alerts = Alert.query.order_by(Alert.timestamp.desc()).all()

    data = []
    for a in alerts:
        data.append({
            "ip": a.ip_address,
            "type": a.attack_type,
            "risk": a.risk_level,
            "time": str(a.timestamp)
        })

    return jsonify(data)

@admin_bp.route('/unblock_ip/<ip>')
def unblock_ip(ip):


    blocked = BlockedIP.query.filter_by(ip_address=ip).first()

    if blocked:
        db.session.delete(blocked)
        db.session.commit()
        print(f"✅ Unblocked IP: {ip}")
    else:
        print(f"⚠️ IP not found: {ip}")

    return redirect(url_for('admin.admin_home'))

@admin_bp.route('/logs')
@login_required
def get_logs():
    logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(5).all()

    data = []
    for log in logs:
        data.append({
            "user_id": log.user_id,
            "action": log.action,
            "time": str(log.timestamp)
        })

    return jsonify(data)

