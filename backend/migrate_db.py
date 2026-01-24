import psycopg2
import os

def migrate_database():
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('POSTGRES_DB', 'quiz_project'),
            user=os.environ.get('POSTGRES_USER', 'admin'),
            password=os.environ.get('POSTGRES_PASSWORD', 'password123'),
            host=os.environ.get('POSTGRES_HOST', 'db'),
            port=os.environ.get('POSTGRES_PORT', '5432')
        )
        cur = conn.cursor()
        
        print("Checking for column 'difficulty_level'...")
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='test_results' AND column_name='difficulty_level';
        """)
        if not cur.fetchone():
            print("Adding 'difficulty_level' column...")
            cur.execute("ALTER TABLE test_results ADD COLUMN difficulty_level INTEGER;")
        else:
            print("'difficulty_level' already exists.")

        print("Checking for column 'results_data'...")
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='test_results' AND column_name='results_data';
        """)
        if not cur.fetchone():
            print("Adding 'results_data' column...")
            cur.execute("ALTER TABLE test_results ADD COLUMN results_data JSONB;")
        else:
            print("'results_data' already exists.")

        conn.commit()
        print("Migration completed successfully!")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate_database()
