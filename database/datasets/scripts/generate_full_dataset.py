import json
import random
import psycopg2

# DB Config
DB_HOST = "localhost"
DB_NAME = "quiz_project"
DB_USER = "admin"
DB_PASS = "password123"
DB_PORT = "5432"

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT)

def clean_answer(answer_text):
    # Take first 100 chars or first line as the "Short Answer" for MCQs to keep it readable
    lines = answer_text.split('\n')
    short_answer = lines[0]
    if len(short_answer) > 200:
        short_answer = short_answer[:200] + "..."
    return short_answer

def main():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Fetch all questions
    cur.execute("SELECT category, difficulty, question, answer FROM questions")
    rows = cur.fetchall()
    
    # Pre-process answers by category to use as distractors
    answers_by_category = {}
    for row in rows:
        cat = row[0]
        ans = clean_answer(row[3])
        if cat not in answers_by_category:
            answers_by_category[cat] = []
        answers_by_category[cat].append(ans)

    dataset = []
    
    for row in rows:
        category, difficulty_str, question_text, answer_text = row
        
        # Map difficulty string to int
        diff_map = {"Beginner": 1, "Intermediate": 3, "Advanced": 5, "Unknown": 3}
        difficulty_int = diff_map.get(difficulty_str, 3)
        
        # Determine Type (70% MCQ/Multi, 30% Open)
        rand_val = random.random()
        
        # Clean the question text (remove markdown boldness)
        clean_q = question_text.replace("**", "").replace("###", "").strip()
        
        q_obj = {
            "category": category,
            "difficulty": difficulty_int,
            "question": clean_q,
            "correct_answer": clean_answer(answer_text),
            "options": None,
            "metadata": {
                "estimated_minutes": 0,
                "tags": [category]
            }
        }
        
        if rand_val < 0.7:
            # Type: Multiple Choice
            q_obj["type"] = "multiple_choice"
            q_obj["metadata"]["estimated_minutes"] = 1
            
            # Generate Distractors: Pick 3 random answers from the SAME category
            possible_distractors = [a for a in answers_by_category.get(category, []) if a != q_obj["correct_answer"]]
            
            # If not enough answers in category, take from global pool or generic
            if len(possible_distractors) < 3:
                 distractors = ["Option A", "Option B", "Option C"] # Fallback
            else:
                distractors = random.sample(possible_distractors, 3)
                
            options = distractors + [q_obj["correct_answer"]]
            random.shuffle(options)
            q_obj["options"] = options
            
        else:
            # Type: Open Ended
            q_obj["type"] = "open_ended"
            q_obj["metadata"]["estimated_minutes"] = 3
            # Keep full answer for open ended reference if needed, 
            # but schema asks for "correct_answer" short ref. We use the cleaned one.
            # OR we can put the full answer for deep checking.
            q_obj["correct_answer"] = answer_text[:500] # logical truncation
        
        dataset.append(q_obj)

    # Save to file
    with open('full_quiz_dataset.json', 'w') as f:
        json.dump(dataset, f, indent=4)
        
    print(f"Successfully generated {len(dataset)} questions in 'full_quiz_dataset.json'.")
    
    # Stats
    mcq_count = sum(1 for x in dataset if x['type'] == 'multiple_choice')
    open_count = sum(1 for x in dataset if x['type'] == 'open_ended')
    print(f"MCQ: {mcq_count} | Open Ended: {open_count}")

    conn.close()

if __name__ == "__main__":
    main()
