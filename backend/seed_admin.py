import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app
from extensions import db
from models.users import User

def seed_admin(username="admin", password=None):
    if password is None:
        password = os.getenv("ADMIN_DEFAULT_PASSWORD", "admin@21")

    with app.app_context():
        db.create_all()

        existing = User.query.filter_by(username=username).first()

        if existing:
            existing.set_password(password)
            existing.role = "admin"
            existing.is_active = True
            db.session.commit()
            print(f"[+] Admin user '{username}' password successfully updated to configured password.")
            return

        admin = User(
            username=username,
            full_name="Dairy Master Admin",
            role="admin",
            is_active=True
        )
        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()
        print(f"[+] Successfully seeded administrator '{username}' with role 'admin' into database.")

if __name__ == "__main__":
    seed_admin()
