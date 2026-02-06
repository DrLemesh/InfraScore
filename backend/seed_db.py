
import psycopg2
import os
import json

def seed_database():
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('DB_NAME', os.environ.get('POSTGRES_DB', 'quiz_project')),
            user=os.environ.get('DB_USER', os.environ.get('POSTGRES_USER', 'admin')),
            password=os.environ.get('DB_PASSWORD', os.environ.get('POSTGRES_PASSWORD', 'password123')),
            host=os.environ.get('DB_HOST', os.environ.get('POSTGRES_HOST', 'db')),
            port=os.environ.get('DB_PORT', os.environ.get('POSTGRES_PORT', '5432'))
        )
        cur = conn.cursor()
        
        # Create quiz_questions table
        print("Creating quiz_questions table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS quiz_questions (
                id SERIAL PRIMARY KEY,
                question_text TEXT NOT NULL,
                question_type VARCHAR(50) NOT NULL,
                options JSONB,
                correct_answer TEXT,
                difficulty_level INTEGER,
                category VARCHAR(100),
                reference_answer TEXT,
                estimated_minutes INTEGER,
                tags JSONB
            );
        """)
        

        # Truncate table to ensure fresh seed
        print("Truncating quiz_questions table...")
        cur.execute("TRUNCATE TABLE quiz_questions RESTART IDENTITY;")
        
        questions = []
        questions = []
        # Potential paths for the dataset (Container vs Local)
        potential_paths = [
            '/app/final_quiz_dataset.json',
            os.path.join(os.path.dirname(__file__), 'final_quiz_dataset.json'),
            os.path.join(os.path.dirname(__file__), '../database/datasets/datasets/final_quiz_dataset.json'),
            'database/datasets/datasets/final_quiz_dataset.json'
        ]
        
        json_file_path = None
        for path in potential_paths:
            if os.path.exists(path):
                json_file_path = path
                break
        
        if json_file_path:
            print(f"Found dataset file: {json_file_path}")
            try:
                with open(json_file_path, 'r') as f:
                    data = json.load(f)
                    
                print(f"Loaded {len(data)} questions from JSON.")
                
                for item in data:
                    # Map JSON fields to DB schema
                    q_type = item.get('type', 'multiple_choice')
                    
                    # Handle answers
                    if q_type == 'open_ended':
                        # Open ended: correct_answer in JSON is actually the reference/explanation
                        db_correct = "Open evaluation"
                        db_ref = item.get('correct_answer', '')
                    else:
                        # Multiple choice: correct_answer is the key/value
                        db_correct = item.get('correct_answer', '')
                        # For MC, we don't have explicit explanation in JSON, so we use correct answer as ref
                        db_ref = f"Correct Answer: {db_correct}"

                    q_obj = {
                        "question_text": item.get('question'),
                        "question_type": q_type,
                        "options": item.get('options'),
                        "correct_answer": db_correct,
                        "difficulty_level": item.get('difficulty', 1),
                        "category": item.get('category', 'General'),
                        "reference_answer": db_ref,
                        "estimated_minutes": item.get('metadata', {}).get('estimated_minutes', 1),
                        "tags": item.get('metadata', {}).get('tags', [])
                    }
                    questions.append(q_obj)
                    
            except Exception as json_err:
                print(f"Error reading JSON dataset: {json_err}. Falling back to hardcoded list.")
                # Fallback logic would go here, but for now we append nothing if failed
            except Exception as json_err:
                print(f"Error reading JSON dataset: {json_err}")
                raise json_err
        else:
            print("Dataset file NOT found in any of the expected paths:")
            for p in potential_paths:
                print(f" - {p}")
            raise FileNotFoundError("Could not find final_quiz_dataset.json")

        print(f"Seeding {len(questions)} questions...")
        
        for q in questions:
            cur.execute("""
                INSERT INTO quiz_questions 
                (question_text, question_type, options, correct_answer, difficulty_level, category, reference_answer, estimated_minutes, tags)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                q['question_text'],
                q['question_type'],
                json.dumps(q['options']) if q['options'] else json.dumps([]), # Handle null options
                json.dumps(q['correct_answer']) if isinstance(q['correct_answer'], list) else q['correct_answer'],
                q['difficulty_level'],
                q['category'],
                q['reference_answer'],
                q.get('estimated_minutes', 2), 
                json.dumps(q.get('tags', []))
            ))
        
        conn.commit()
        print("Database transaction committed.")
        
        cur.close()
        conn.close()



        

        
    except Exception as e:
        print(f"Error seeding database: {e}")

if __name__ == "__main__":
    seed_database()
