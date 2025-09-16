#!/usr/bin/env python3
"""
Script to create an admin user
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User

def create_admin_user():
    with app.app_context():
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            admin_user.is_admin = True
            db.session.commit()
            print(f"✅ User 'admin' already exists and is now an admin!")
        else:
            # Create new admin user
            admin_user = User(
                username='admin',
                email='admin@tukonect.com',
                is_admin=True,
                is_active=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print(f"✅ Created admin user:")
            print(f"   Username: admin")
            print(f"   Email: admin@tukonect.com")
            print(f"   Password: admin123")
            print(f"   You can now login with these credentials to access admin features.")

if __name__ == "__main__":
    create_admin_user()
