#!/usr/bin/env python3
"""
Script to make a user an admin
Usage: python make_admin.py <username>
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User

def make_admin(username):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            user.is_admin = True
            db.session.commit()
            print(f"✅ User '{username}' is now an admin!")
        else:
            print(f"❌ User '{username}' not found!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python make_admin.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    make_admin(username)
