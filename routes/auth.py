from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from extension import db, bcrypt
from models import User, ActivityLog
from datetime import datetime
from functools import wraps
from models import Alert
from flask import current_app
from flask import session

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET', 'POST'])
# @auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # ip = request.remote_addr
        
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        if ip and "," in ip:
            ip = ip.split(",")[0].strip()

        user = User.query.filter_by(username=username).first()

        # 🚫 User not found
        if not user:
            flash("Invalid credentials", "danger")
            return redirect(url_for('auth.login'))

        # 🔒 Account locked
        if user.is_locked:
            flash("Account locked due to multiple failed attempts", "danger")
            return redirect(url_for('auth.login'))

        # 🔑 Password check
        if bcrypt.check_password_hash(user.password, password):
            user.failed_attempts = 0
            db.session.commit()
            
            current_app.ids.failed_logins[ip] = []

            login_user(user)

            # 📊 Log activity
            log = ActivityLog(
                user_id=user.id,
                action="Login Success",
                ip_address=ip
            )
            db.session.add(log)
            db.session.commit()

            # 🔀 Role-based redirect
            if user.role == "admin":
                return redirect(url_for('admin.admin_home'))
            elif user.role == "doctor":
                return redirect(url_for('doctor.doctor_home'))
            elif user.role == "reception":
                return redirect(url_for('reception.reception_home'))

        else:
            # ❌ Failed login
            user.failed_attempts += 1

            # 🚨 Lock account after threshold
            if user.failed_attempts >= 5:
                user.is_locked = True
                flash("Account locked due to multiple failed attempts", "danger")
            else:
                flash("Invalid credentials", "danger")

            db.session.commit()

            # 📊 Log failed attempt
            log = ActivityLog(
                user_id=user.id,
                action="Login Failed",
                ip_address=ip
            )
            db.session.add(log)
            db.session.commit()
            
            
            # 🛡️ IDS Brute Force Detection (NEW)
        blocked = current_app.ids.record_failed_login(ip)
        if blocked:
            return "Blocked: Too many failed login attempts (IDS)", 403

        return redirect(url_for('auth.login'))

    return render_template("login.html")


@auth_bp.route('/logout')
@login_required
def logout():
    ip = request.remote_addr

    # Log logout
    log = ActivityLog(
        user_id=current_user.id,
        action="Logout",
        ip_address=ip
    )
    db.session.add(log)
    db.session.commit()

    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))


def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator


