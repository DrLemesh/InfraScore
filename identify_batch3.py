import json
import psycopg2
import os

def identify_next_batch():
    # 1. Get current DB state to see what needs fixing
    # (Since I updated DB directly, I should check DB state, not just JSON)
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'quiz_project'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'password123')
    )
    cur = conn.cursor()
    cur.execute("SELECT id, question_text, correct_answer, options FROM quiz_questions")
    rows = cur.fetchall()
    
    candidates = []
    
    for row in rows:
        qid, txt, correct, opts = row
        if not opts or len(opts) < 2: continue
        
        # Check if correct is strictly longest
        sorted_opts = sorted(opts, key=len, reverse=True)
        longest = sorted_opts[0]
        second = sorted_opts[1]
        
        if longest == correct and len(longest) > len(second):
            # Calculate "obviousness" score
            diff = len(longest) - len(second)
            # Only care if diff is significant, e.g. > 10 chars
            if diff > 10:
                candidates.append({
                    'id': qid,
                    'text': txt,
                    'correct': correct,
                    'diff': diff
                })
                
    # Sort by diff desc
    candidates.sort(key=lambda x: x['diff'], reverse=True)
    
    # Dump top 50
    print(f"Found {len(candidates)} remaining candidates.")
    with open('next_batch_fix.json', 'w') as f:
        json.dump(candidates[:50], f, indent=2)
        
    cur.close()
    conn.close()

if __name__ == "__main__":
    identify_next_batch()
