import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect('autoq.db')
cursor = conn.cursor()

# Check if user exists
cursor.execute("SELECT id FROM users WHERE id = 1")
existing = cursor.fetchone()

if not existing:
    # Insert default user
    # Password hash for "default123"
    cursor.execute("""
        INSERT INTO users (id, email, username, hashed_password, full_name, role, is_active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        1,
        'default@autoq.local',
        'default',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIxj3qOz7a',
        'Default User',
        'instructor',
        1,
        datetime.now().isoformat(),
        datetime.now().isoformat()
    ))
    conn.commit()
    print("OK: Default user created!")
    print("   Username: default")
    print("   Password: default123")
else:
    print("INFO: Default user already exists")

conn.close()
