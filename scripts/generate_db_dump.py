import psycopg2
import json

# DB Config
DB_HOST = "localhost"
DB_NAME = "quiz_project"
DB_USER = "admin"
DB_PASS = "password123"
DB_PORT = "5432"

OUTPUT_FILE = "clean_database_dump.txt"

def main():
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT)
        cur = conn.cursor()

        cur.execute("SELECT * FROM questions ORDER BY id")
        rows = cur.fetchall()

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            for row in rows:
                # schema: id, category, type, difficulty, question, correct_answer, options, metadata, created_at
                f.write(f"ID: {row[0]}\n")
                f.write(f"Category: {row[1]}\n")
                f.write(f"Type: {row[2]}\n")
                f.write(f"Difficulty: {row[3]}\n")
                f.write(f"Question: {row[4]}\n")
                f.write(f"Answer: {row[5]}\n")
                f.write(f"Options: {json.dumps(row[6])}\n")
                f.write(f"Metadata: {json.dumps(row[7])}\n")
                f.write("-" * 40 + "\n")
        
        print(f"Successfully exported {len(rows)} questions to {OUTPUT_FILE}")
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
