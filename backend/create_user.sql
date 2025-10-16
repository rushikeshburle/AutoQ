-- Create default user for AutoQ
INSERT OR IGNORE INTO users (id, email, username, hashed_password, full_name, role, is_active, created_at, updated_at)
VALUES (
    1,
    'default@autoq.local',
    'default',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIxj3qOz7a',
    'Default User',
    'instructor',
    1,
    datetime('now'),
    datetime('now')
);
