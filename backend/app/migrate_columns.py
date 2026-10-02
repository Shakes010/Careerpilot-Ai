from app.database import engine
from sqlalchemy import text

def run_migration():
    with engine.connect() as conn:
        print("Migrating database columns...")
        conn.execute(text("ALTER TABLE assessments ADD COLUMN IF NOT EXISTS is_language_flexible BOOLEAN DEFAULT false;"))
        conn.execute(text("ALTER TABLE checkpoint_submissions ADD COLUMN IF NOT EXISTS language VARCHAR(50);"))
        conn.commit()
        print("Database schema migration completed successfully.")

if __name__ == "__main__":
    run_migration()
