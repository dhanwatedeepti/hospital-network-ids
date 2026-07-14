from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extension import db
from models import Patient
from models import User
from datetime import datetime
from flask_login import current_user
from utils import log_activity
from flask import flash


reception_bp = Blueprint('reception', __name__)
# -----------------------------
# 🏥 RECEPTION DASHBOARD
# -----------------------------
@reception_bp.route('/reception')
@login_required
def reception_home():
    if current_user.role != "reception":
        return "Access Denied", 403

    
    patients = Patient.query.order_by(Patient.created_at.desc()).all()
    return render_template("dashboard_reception.html", patients=patients)


# -----------------------------
# ➕ ADD PATIENT
# -----------------------------
@reception_bp.route('/add_patient', methods=['POST'])
@login_required
def add_patient():
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    phone = request.form.get('phone')
    address = request.form.get('address')
    medical_history = request.form.get('medical_history')

    new_patient = Patient(
        name=name,
        age=age,
        gender=gender,
        phone=phone,
        address=address,
        medical_history=medical_history
        
    )

    db.session.add(new_patient)
    db.session.commit()
    log_activity("Added new patient")

    return redirect(url_for('reception.reception_home'))

# @reception_bp.route('/book_appointment', methods=['POST'])
# @login_required
# def book_appointment():

#     patient_id = request.form.get("patient_id")
#     doctors = User.query.filter_by(role="doctor").all()
#     return render_template(
#     "reception_dashboard.html",
#     doctors=doctors
#           )


    # return redirect(url_for('reception.reception_home'))
