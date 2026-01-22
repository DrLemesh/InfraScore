
import psycopg2
import os
import time

def check_questions():
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('POSTGRES_DB', 'quiz_project'),
            user=os.environ.get('POSTGRES_USER', 'admin'),
            password=os.environ.get('POSTGRES_PASSWORD', 'password123'),
            host=os.environ.get('POSTGRES_HOST', 'db'),  # Changed to 'db'
            port=os.environ.get('POSTGRES_PORT', '5432')
        )
        cur = conn.cursor()
        
        # Check total count
        try:
            cur.execute("SELECT count(*) FROM quiz_questions;")
            total = cur.fetchone()[0]
            print(f"Total questions in database: {total}")
            
            if total == 0:
                print("WARNING: Database is empty!")
            else:
                # Check count by difficulty
                cur.execute("""
                    SELECT difficulty_level, count(*) 
                    FROM quiz_questions 
                    GROUP BY difficulty_level 
                    ORDER BY difficulty_level;
                """)
                rows = cur.fetchall()
                print("\nQuestions by difficulty:")
                for row in rows:
                    print(f"Level {row[0]}: {row[1]} questions")
        except psycopg2.errors.UndefinedTable:
             print("ERROR: table 'quiz_questions' does not exist!")
             
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error connecting to database: {e}")

if __name__ == "__main__":
    check_questions()
