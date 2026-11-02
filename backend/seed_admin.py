import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app
from extensions import db
from models.users import User

def seed_admin():
    with app.app_context():
        db.create_all()

        admin_username = "admin"
        existing = User.query.filter_by(username=admin_username).first()

        if existing:
            print(f"[*] Admin user '{admin_username}' already exists in database (Role: {existing.role}).")
            return

        admin = User(
            username=admin_username,
            full_name="Dairy Master Admin",
            role="admin",
            is_active=True
        )
        admin.set_password("admin@123")

        db.session.add(admin)
        db.session.commit()
        print(f"[+] Successfully seeded default admin user '{admin_username}' with role 'admin' into database!")

if __name__ == "__main__":
    seed_admin()
