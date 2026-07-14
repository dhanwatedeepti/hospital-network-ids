from app import create_app
from extension import db, bcrypt
from models import User

app = create_app()

with app.app_context():
    # User.query.filter_by(username="admin").delete()
    User.query.delete()
    db.session.commit()

    # hashed_pw = bcrypt.generate_password_hash("admin123").decode("utf-8")

    admin = User(
        username="admin",
        email="admin@hospital.com",
        password=bcrypt.generate_password_hash("admin123").decode("utf-8"),
        role="admin",
        is_locked=False,
        failed_attempts=0
    )

   # 👨‍⚕️ Doctor
    doctor = User(
        username="doctor",
        email="doctor@hospital.com",
        password=bcrypt.generate_password_hash("doc123").decode("utf-8"),
        role="doctor",
        is_locked=False,
        failed_attempts=0
    )

    # 🧾 Receptionist
    reception = User(
        username="reception",
        email="reception@hospital.com",
        password=bcrypt.generate_password_hash("rec123").decode("utf-8"),
        role="reception",
        is_locked=False,
        failed_attempts=0
    )

    db.session.add_all([admin, doctor, reception])
    db.session.commit()

    print("Users created successfully")
