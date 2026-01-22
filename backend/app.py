import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from flask_bcrypt import Bcrypt
import os
import secrets

# Get absolute path to the frontend/templates directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'frontend', 'templates')

app = Flask(__name__, template_folder=template_dir)

# Configure session
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize Bcrypt
bcrypt = Bcrypt(app)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'quiz_project'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'password123')
    )
    return conn

def hash_password(password):
    """Hash a password using bcrypt."""
    return bcrypt.generate_password_hash(password).decode('utf-8')

def verify_password(password, password_hash):
    """Verify a password against its hash."""
    return bcrypt.check_password_hash(password_hash, password)

def get_user_by_email(email):
    """Retrieve a user by email address."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

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
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['fullname', 'username', 'email', 'password', 'role', 'status', 'experience']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if user already exists
        existing_user = get_user_by_email(data['email'])
        if existing_user:
            return jsonify({'error': 'An account with this email already exists'}), 400
        
        # Hash the password
        password_hash = hash_password(data['password'])
        
        # Insert user into database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users (username, email, password_hash, created_at)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING id
            """,
            (data['username'], data['email'], password_hash)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        # Create session
        session['user_id'] = user_id
        session['email'] = data['email']
        session['username'] = data['username']
        session['fullname'] = data['fullname']
        
        return jsonify({'success': True, 'message': 'Account created successfully'}), 201
        
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'error': 'An error occurred during registration'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Get user from database
        user = get_user_by_email(email)
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create session
        session['user_id'] = user['id']
        session['email'] = user['email']
        session['username'] = user['username']
        
        return jsonify({'success': True, 'message': 'Login successful'}), 200
        
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': 'An error occurred during login'}), 500

@app.route('/api/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

@app.route('/api/current-user')
def current_user():
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'user_id': session['user_id'],
            'email': session['email'],
            'username': session['username']
        })
    return jsonify({'logged_in': False})

@app.route('/quiz-menu')
def quiz_menu():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('quiz-menu.html')

@app.route('/quiz')

def quiz():
    return render_template('question-tab.html')



@app.route('/api/generate-quiz', methods=['POST'])
def generate_quiz():
    """Generate a new quiz based on user-selected parameters"""
    try:
        # Check if user is logged in
        if 'user_id' not in session:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        question_count = int(data.get('count', 15))
        difficulty_level = int(data.get('difficulty', 3))
        
        # Validate parameters
        if question_count < 1 or question_count > 50:
            return jsonify({'error': 'Question count must be between 1 and 50'}), 400
        if difficulty_level < 1 or difficulty_level > 5:
            return jsonify({'error': 'Difficulty level must be between 1 and 5'}), 400
        
        # Query database for random questions matching criteria
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
        SELECT id, question_text, question_type, options, correct_answer, 
               difficulty_level, category, reference_answer, estimated_minutes
        FROM quiz_questions 
        WHERE difficulty_level = %s
        ORDER BY RANDOM() 
        LIMIT %s;
        """
        
        cur.execute(query, (difficulty_level, question_count))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        if len(rows) == 0:
            return jsonify({'error': f'No questions found for difficulty level {difficulty_level}'}), 404
        
        # Convert rows to dictionaries
        questions = []
        for row in rows:
            questions.append({
                'id': row[0],
                'question_text': row[1],
                'question_type': row[2],
                'options': row[3],
                'correct_answer': row[4],
                'difficulty_level': row[5],
                'category': row[6],
                'reference_answer': row[7],
                'estimated_minutes': row[8]
            })
        
        # Store quiz in session
        session['quiz_questions'] = questions
        session['current_question_index'] = 0
        session['user_answers'] = {}
        session['quiz_difficulty'] = difficulty_level
        session['quiz_count'] = len(questions)
        
        return jsonify({
            'success': True,
            'message': f'Quiz generated with {len(questions)} questions',
            'question_count': len(questions),
            'difficulty': difficulty_level
        }), 201
        
    except Exception as e:
        print(f"Quiz generation error: {e}")
        return jsonify({'error': 'Failed to generate quiz'}), 500

@app.route('/api/quiz/current-question', methods=['GET'])
def get_current_question():
    """Get the current question in the active quiz"""
    try:
        # Check if quiz exists in session
        if 'quiz_questions' not in session:
            return jsonify({'error': 'No active quiz found'}), 404
        
        questions = session['quiz_questions']
        current_index = session.get('current_question_index', 0)
        
        if current_index >= len(questions):
            return jsonify({'error': 'Quiz completed', 'completed': True}), 200
        
        current_question = questions[current_index]
        user_answers = session.get('user_answers', {})
        
        return jsonify({
            'question': current_question,
            'current_index': current_index,
            'total_questions': len(questions),
            'saved_answer': user_answers.get(str(current_index)),
            'is_last': current_index == len(questions) - 1
        }), 200
        
    except Exception as e:
        print(f"Error fetching question: {e}")
        return jsonify({'error': 'Failed to fetch question'}), 500

@app.route('/api/quiz/navigate', methods=['POST'])
def navigate_question():
    """Navigate to a specific question by index"""
    try:
        if 'quiz_questions' not in session:
            return jsonify({'error': 'No active quiz found'}), 404
        
        data = request.get_json()
        new_index = int(data.get('index', 0))
        
        questions = session['quiz_questions']
        
        if new_index < 0 or new_index >= len(questions):
            return jsonify({'error': 'Invalid question index'}), 400
        
        session['current_question_index'] = new_index
        
        return jsonify({
            'success': True,
            'current_index': new_index
        }), 200
        
    except Exception as e:
        print(f"Navigation error: {e}")
        return jsonify({'error': 'Failed to navigate'}), 500

@app.route('/api/quiz/submit-answer', methods=['POST'])
def submit_answer():
    """Submit an answer for the current question"""
    try:
        if 'quiz_questions' not in session:
            return jsonify({'error': 'No active quiz found'}), 404
        
        data = request.get_json()
        answer = data.get('answer')
        current_index = session.get('current_question_index', 0)
        
        # Save answer in session
        if 'user_answers' not in session:
            session['user_answers'] = {}
        
        session['user_answers'][str(current_index)] = answer
        session.modified = True
        
        return jsonify({
            'success': True,
            'message': 'Answer saved'
        }), 200
        
    except Exception as e:
        print(f"Answer submission error: {e}")
        return jsonify({'error': 'Failed to save answer'}), 500

@app.route('/api/quiz/results', methods=['GET'])
def get_quiz_results():
    """Calculate and return quiz results"""
    try:
        if 'quiz_questions' not in session:
            return jsonify({'error': 'No active quiz found'}), 404
        
        questions = session['quiz_questions']
        user_answers = session.get('user_answers', {})
        
        correct_count = 0
        results_breakdown = []
        
        for i, question in enumerate(questions):
            user_answer = user_answers.get(str(i))
            correct_answer = question['correct_answer']
            
            is_correct = False
            if question['question_type'] == 'multi_select':
                # For multi-select, compare as sets
                if user_answer and correct_answer:
                    is_correct = set(user_answer) == set(correct_answer)
            else:
                # For single answer questions
                is_correct = user_answer == correct_answer
            
            if is_correct:
                correct_count += 1
            
            results_breakdown.append({
                'question_number': i + 1,
                'question_text': question['question_text'],
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'category': question.get('category'),
                'reference_answer': question.get('reference_answer')
            })
        
        total_questions = len(questions)
        percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
        # Optionally save results to database
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO test_results (user_id, score, total_questions, completed_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                """,
                (session['user_id'], correct_count, total_questions)
            )
            conn.commit()
            cur.close()
            conn.close()
        except Exception as db_error:
            print(f"Error saving results to database: {db_error}")
        
        # Clear quiz from session
        session.pop('quiz_questions', None)
        session.pop('current_question_index', None)
        session.pop('user_answers', None)
        
        return jsonify({
            'score': correct_count,
            'total_questions': total_questions,
            'percentage': round(percentage, 2),
            'results_breakdown': results_breakdown
        }), 200
        
    except Exception as e:
        print(f"Results calculation error: {e}")
        return jsonify({'error': 'Failed to calculate results'}), 500

@app.route('/generate-exam', methods=['GET'])
def generate_exam():
    """Legacy endpoint - kept for backward compatibility"""
    conn = get_db_connection()
    cur = conn.cursor()
    
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
    
    exam_questions = []
    for row in rows:
        exam_questions.append({
            'question': row[0],
            'type': row[1],
            'difficulty': row[2],
            'options': row[3],
            'correct_answer': row[4]
        })
    
    return jsonify(exam_questions)


@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get user statistics and AI analysis for dashboard"""
    try:
        # Check if user is logged in
        if 'user_id' not in session:
            return jsonify({'error': 'User not authenticated'}), 401
            
        user_id = session['user_id']
        conn = get_db_connection()
        cur = conn.cursor(psycopg2.extras.RealDictCursor) # Use RealDictCursor to easier json serialization
        
        # 1. Fetch recent results
        cur.execute("""
            SELECT score, total_questions, completed_at
            FROM test_results
            WHERE user_id = %s
            ORDER BY completed_at DESC
            LIMIT 10
        """, (user_id,))
        recent_results = cur.fetchall()
        
        # 2. Calculate stats
        total_quizzes = len(recent_results)
        if total_quizzes > 0:
            total_score_sum = sum([r['score'] for r in recent_results])
            total_max_sum = sum([r['total_questions'] for r in recent_results])
            average_percentage = (total_score_sum / total_max_sum * 100) if total_max_sum > 0 else 0
            
            # Format history for frontend
            history = []
            for r in recent_results:
                history.append({
                    'score': r['score'],
                    'total': r['total_questions'],
                    'date': r['completed_at'].strftime('%Y-%m-%d %H:%M'),
                    'percentage': round((r['score'] / r['total_questions'] * 100), 1)
                })
        else:
            average_percentage = 0
            history = []
            
        cur.close()
        conn.close()
        
        # 3. Generate "AI Analysis" (Mock/Rule-based for now)
        analysis = {
            'level': 'Beginner',
            'summary': 'Start taking quizzes to generate analysis.',
            'strengths': ['N/A'],
            'weaknesses': ['N/A']
        }
        
        if total_quizzes > 0:
            if average_percentage >= 85:
                analysis['level'] = 'Expert'
                analysis['summary'] = "Exception performance! You're demonstrating senior-level DevOps knowledge."
                analysis['strengths'] = ["Consistency", "High Score Retention"]
                analysis['weaknesses'] = ["Keep challenging yourself with Level 5 questions"]
            elif average_percentage >= 70:
                analysis['level'] = 'Intermediate'
                analysis['summary'] = "Good solid progress. You have a strong grasp of the basics but can improve consistency."
                analysis['strengths'] = ["General Knowledge"]
                analysis['weaknesses'] = ["Complex Scenarios", "Edge Cases"]
            elif average_percentage >= 50:
                analysis['level'] = 'Junior'
                analysis['summary'] = "You're getting there! Focus on understanding core concepts before moving to advanced topics."
                analysis['strengths'] = ["Basic Terminology"]
                analysis['weaknesses'] = ["System Architecture", "Deployment Strategies"]
            else:
                analysis['level'] = 'Beginner'
                analysis['summary'] = "Early stages of learning. Recommend reviewing the curriculum and starting with Level 1 quizzes."
                analysis['strengths'] = ["Starting the Journey"]
                analysis['weaknesses'] = ["Fundamentals", "Command Line Basics"]
                
        return jsonify({
            'stats': {
                'quizzes_taken': total_quizzes,
                'average_score': round(average_percentage, 1),
                'history': history
            },
            'analysis': analysis
        })
        
    except Exception as e:
        print(f"Dashboard stats error: {e}")
        return jsonify({'error': 'Failed to fetch dashboard stats'}), 500


if __name__ == "__main__":
    try:
        create_tables()
    except Exception as e:
        print(f"Error creating tables: {e}")
    app.run(debug=True, host='0.0.0.0')