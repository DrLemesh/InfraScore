import json
import psycopg2
import os

def ingest_data():
    # חיבור ל-DB (וודא שהקונטיינר של ה-DB רץ!)
    conn = psycopg2.connect(
        host='localhost',
        database='quiz_project',
        user='admin',
        password='password123'
    )
    cur = conn.cursor()

    # Create Table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id SERIAL PRIMARY KEY,
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
    conn.commit()

    # Calculate path to dataset relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(script_dir, '..', 'datasets', 'final_quiz_dataset.json')

    # Load the JSON file
    with open(dataset_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    for q in questions:
        # Note: 'category' and 'correct_answer' are NOT NULL in the DB, so we provide defaults if missing
        cur.execute(
            """
            INSERT INTO quiz_questions (question, type, difficulty, options, category, correct_answer) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                q.get('question', q.get('content')), # Support both keys
                q.get('type', q.get('question_type')), 
                q['difficulty'], 
                json.dumps(q.get('options', [])),
                q.get('category', 'General'), # Default category
                q.get('correct_answer', '')   # Default empty answer
            )
        )
    
    conn.commit()
    print(f"Successfully ingested {len(questions)} questions!")
    cur.close()
    conn.close()

if __name__ == "__main__":
    ingest_data()