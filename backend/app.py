import psycopg2
from flask import Flask, jsonify, render_template
import os

# Get absolute path to the frontend/templates directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'frontend', 'templates')

app = Flask(__name__, template_folder=template_dir)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'quiz_project'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'password123')
    )
    return conn

def create_tables():
    """Initialize the database with required tables."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create Users Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Create Test Results Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            completed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("Database tables created successfully.")

@app.route('/')
def landing():
    return render_template('landing-page.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/quiz')
def quiz():
    return render_template('question-tab.html')


@app.route('/generate-exam', methods=['GET'])
def generate_exam():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Updated to select correct_answer as well
    query = """
    SELECT question, type, difficulty, options, correct_answer
    FROM quiz_questions 
    ORDER BY RANDOM() 
    LIMIT 10;
    """
    
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    # turning the rows into a list of dictionaries
    exam_questions = []
    for row in rows:
        exam_questions.append({
            'question': row[0],
            'type': row[1],
            'difficulty': row[2],
            'options': row[3], # options is already JSONB/dict from psycopg2
            'correct_answer': row[4]
        })
    
    return jsonify(exam_questions)

if __name__ == '__main__':
    try:
        create_tables()
    except Exception as e:
        print(f"Error creating tables: {e}")
    app.run(debug=True, host='0.0.0.0')