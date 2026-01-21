import os
import psycopg2
import re

# DB Config
DB_HOST = "localhost"
DB_NAME = "quiz_project"
DB_USER = "admin"
DB_PASS = "password123"
DB_PORT = "5432"

BASE_DIR = "DevOps-Interview-Questions"

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT)
    return conn

def create_table(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id SERIAL PRIMARY KEY,
            category TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            CONSTRAINT unique_question_category UNIQUE (category, question)
        );
    """)
    conn.commit()
    cur.close()

def parse_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.readlines()

    questions = []
    current_question = None
    current_answer = []
    
    # "Unknown" is default if no header is found
    current_difficulty = "Unknown"

    for line in content:
        stripped_line = line.strip()
        
        # Detect Difficulty Header
        if stripped_line.startswith("## ") and "Beginner" in stripped_line:
            current_difficulty = "Beginner"
            continue
        elif stripped_line.startswith("## ") and "Intermediate" in stripped_line:
            current_difficulty = "Intermediate"
            continue
        elif stripped_line.startswith("## ") and "Advanced" in stripped_line:
            current_difficulty = "Advanced"
            continue
            
        # Look for third-level headers as questions
        if stripped_line.startswith("###"):
            # Save the previous question if it exists
            if current_question:
                questions.append({
                    "difficulty": current_difficulty,
                    "question": current_question,
                    "answer": "\n".join(current_answer).strip()
                })
            # Start a new question
            clean_question = stripped_line.lstrip("#").strip()
            current_question = clean_question
            current_answer = []
        elif current_question:
            current_answer.append(line)
    
    # Add the last question
    if current_question:
        questions.append({
            "difficulty": current_difficulty,
            "question": current_question,
            "answer": "\n".join(current_answer).strip()
        })
    
    return questions

def main():
    try:
        conn = get_db_connection()
        print("Connected to database.")
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return

    create_table(conn)
    cur = conn.cursor()

    count = 0
    # Walk through directories
    for root, dirs, files in os.walk(BASE_DIR):
        if "README.md" in files:
            # Skip the root README
            if os.path.abspath(root) == os.path.abspath(BASE_DIR):
                continue
            
            category = os.path.basename(root)
            if category.startswith("."):
                continue

            file_path = os.path.join(root, "README.md")
            print(f"Processing category: {category}...")
            
            parsed_data = parse_markdown(file_path)
            
            for item in parsed_data:
                if not item['question'] or not item['answer']:
                    continue

                cur.execute(
                    """
                    INSERT INTO questions (category, difficulty, question, answer) 
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (category, question) DO NOTHING
                    """,
                    (category, item['difficulty'], item['question'], item['answer'])
                )
                if cur.rowcount > 0:
                    count += 1
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"Successfully inserted {count} new questions into the database.")

if __name__ == "__main__":
    main()
