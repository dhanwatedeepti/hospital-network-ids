from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Patient, db
from utils import log_activity


doctor_bp = Blueprint('doctor', __name__)
# log_activity("Updated patient record")
# -----------------------------
# 🧑‍⚕️ DOCTOR DASHBOARD
# -----------------------------
@doctor_bp.route('/doctor')
@login_required
def doctor_home():
    
    if current_user.role != "doctor":
        return "Access Denied", 403


    patients = Patient.query.all()
    return render_template(
        "dashboard_doctor.html",
        patients=patients
    )


# -----------------------------
# ✍️ UPDATE PATIENT RECORD
# -----------------------------
@doctor_bp.route('/update_patient/<int:pid>', methods=['POST'])
@login_required
def update_patient(pid):

    patient = Patient.query.get_or_404(pid)

    patient.medical_history = request.form.get("medical_history")
    patient.doctor_notes = request.form.get("doctor_notes")
    patient.updated_by = current_user.id

    db.session.commit()
    log_activity("Updated patient record")
    
    return redirect(url_for('doctor.doctor_home'))