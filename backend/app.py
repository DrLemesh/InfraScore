import psycopg2
from flask import Flask, jsonify, render_template
import os

# Get absolute path to the frontend/templates directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'frontend', 'templates')

app = Flask(__name__, template_folder=template_dir)

def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='quiz_project',
        user='admin',
        password='password123'
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

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
    app.run(debug=True)