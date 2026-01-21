import json
import psycopg2
from psycopg2.extras import Json

# DB Config
DB_HOST = "localhost"
DB_NAME = "quiz_project"
DB_USER = "admin"
DB_PASS = "password123"
DB_PORT = "5432"

def main():
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT)
        cur = conn.cursor()

        # Create Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS quiz_questions (
                id INTEGER PRIMARY KEY,
                category TEXT NOT NULL,
                type TEXT NOT NULL,
                difficulty INTEGER NOT NULL,
                question TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                options JSONB,
                metadata JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Truncate to ensure clean import
        cur.execute("TRUNCATE TABLE quiz_questions RESTART IDENTITY;")
        print("Table 'quiz_questions' created/truncated.")

        # Read Data
        with open("final_quiz_dataset.json", 'r') as f:
            data = json.load(f)

        # Insert Data
        count = 0
        for item in data:
            cur.execute("""
                INSERT INTO quiz_questions (id, category, type, difficulty, question, correct_answer, options, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                item['id'],
                item['category'],
                item['type'],
                item['difficulty'],
                item['question'],
                item['correct_answer'],
                Json(item['options']),
                Json(item['metadata'])
            ))
            count += 1

        conn.commit()
        print(f"Successfully inserted {count} questions into 'quiz_questions'.")
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
