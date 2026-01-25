import json

def identify():
    with open('questions_dump.json', 'r') as f:
        questions = json.load(f)
        
    problematic = []
    
    for q in questions:
        opts = q.get('options', [])
        correct = q.get('correct_answer', "")
        
        if not opts or len(opts) < 2:
            continue
            
        # Check if correct answer is in options
        if correct not in opts:
            # Maybe slight mismatch, but for now skip
            continue
            
        sorted_opts = sorted(opts, key=len, reverse=True)
        longest = sorted_opts[0]
        second_longest = sorted_opts[1]
        
        # If correct answer is the longest, and notably longer (e.g. > 5 chars difference) or just strictly longest
        # User said "answer is the longest", so strictly longest is the criteria.
        
        if longest == correct and len(longest) > len(second_longest):
            problematic.append({
                'id': q['id'],
                'text': q['question_text'],
                'correct': correct,
                'current_options': opts
            })
            
    # Save to file
    with open('problematic_questions.json', 'w') as f:
        json.dump(problematic, f, indent=2)
        
    print(f"Found {len(problematic)} problematic questions.")

if __name__ == '__main__':
    identify()
