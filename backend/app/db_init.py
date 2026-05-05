"""
Database initialization and seeding script.
Run once to create tables: python -m app.db_init
"""
from app import create_app, db

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("[OK] Database tables created successfully.")

if __name__ == "__main__":
    init_db()
