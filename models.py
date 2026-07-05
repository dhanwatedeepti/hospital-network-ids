from datetime import datetime, timezone
from extension import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from zoneinfo import ZoneInfo


# -----------------------------
# 🔐 USER MODEL (AUTH SYSTEM)
# -----------------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # admin, doctor, receptionist

    is_locked = db.Column(db.Boolean, default=False)
    failed_attempts = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


#IP blocking model 
class BlockedIP(db.Model):
    __tablename__ = "blocked_ips"

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50), unique=True)
    reason = db.Column(db.String(100))
    timestamp = db.Column(
    db.DateTime,
    default=lambda: datetime.now(ZoneInfo("Asia/Kolkata"))
    )

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -----------------------------
# 🏥 PATIENT MODEL
# -----------------------------
class Patient(db.Model):
    __tablename__ = "patients"

    # class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(15))
    address = db.Column(db.String(200))
    medical_history = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    doctor_notes = db.Column(db.Text)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    def __repr__(self):
        return f"<Patient {self.name}>"


# -----------------------------
# 🚨 IDS ALERT MODEL
# -----------------------------
class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)

    ip_address = db.Column(db.String(50), nullable=False)
    attack_type = db.Column(db.String(100), nullable=False)
    risk_level = db.Column(db.String(20))  # Low, Medium, High

    endpoint = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="alerts")

    def __repr__(self):
        return f"<Alert {self.attack_type} from {self.ip_address}>"


# -----------------------------
# 📊 ACTIVITY LOG MODEL
# -----------------------------
class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    action = db.Column(db.String(255))
    ip_address = db.Column(db.String(50))


    timestamp = db.Column(
    db.DateTime,
    default=lambda: datetime.now(ZoneInfo("Asia/Kolkata"))
    )
    user = db.relationship("User", backref="activities")

    def __repr__(self):
        return f"<Activity {self.action} by User {self.user_id}>"
    
    
    