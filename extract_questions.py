import psycopg2
import json
import os

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'quiz_project'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'password123')
    )

def extract_questions():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, question_text, correct_answer, options FROM quiz_questions;")
        rows = cur.fetchall()
        
        questions = []
        for row in rows:
            questions.append({
                'id': row[0],
                'question_text': row[1],
                'correct_answer': row[2],
                'options': row[3]
            })
            
        with open('questions_dump.json', 'w') as f:
            json.dump(questions, f, indent=2)
            
        print(f"Extracted {len(questions)} questions.")
        
        # Quick analysis
        first_is_correct = 0
        longest_is_correct = 0
        
        for q in questions:
            opts = q['options']
            correct = q['correct_answer']
            
            if opts and opts[0] == correct:
                first_is_correct += 1
                
            sorted_by_len = sorted(opts, key=len, reverse=True)
            if sorted_by_len and sorted_by_len[0] == correct:
                # specific check: is it strictly longer than the second one?
                if len(opts) > 1 and len(sorted_by_len[0]) > len(sorted_by_len[1]):
                    longest_is_correct += 1

        print(f"Stats:")
        print(f"Correct answer is first option: {first_is_correct}/{len(questions)} ({first_is_correct/len(questions)*100:.1f}%)")
        print(f"Correct answer is strictly longest: {longest_is_correct}/{len(questions)} ({longest_is_correct/len(questions)*100:.1f}%)")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    extract_questions()
