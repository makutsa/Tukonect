#!/usr/bin/env python3
"""
Script to make the first user an admin
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User

def make_first_user_admin():
    with app.app_context():
        # Get the first user
        first_user = User.query.first()
        if first_user:
            first_user.is_admin = True
            db.session.commit()
            print(f"✅ User '{first_user.username}' (ID: {first_user.id}) is now an admin!")
            print(f"   Email: {first_user.email}")
            print(f"   You can now login as this user to access admin features.")
        else:
            print("❌ No users found in the database!")
            print("   Please register a user first, then run this script again.")

if __name__ == "__main__":
    make_first_user_admin()
