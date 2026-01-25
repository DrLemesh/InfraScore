import json
import os
import glob

def analyze():
    files = glob.glob('database/datasets/datasets/*.json')
    all_problems = []
    seen_questions = set()

    for fpath in files:
        with open(fpath, 'r') as f:
            try:
                data = json.load(f)
                # Handle list or dict wrapper
                if isinstance(data, dict):
                    # Some files might have 'questions' key? check structure later if needed
                    # prioritizing list components
                    pass
                
                # Assume list of questions for now based on previous interactions
                if not isinstance(data, list):
                    continue

                for q in data:
                    q_text = q.get('question_text') or q.get('question')
                    if not q_text or q_text in seen_questions:
                        continue
                    
                    seen_questions.add(q_text)
                    
                    correct = q.get('correct_answer')
                    options = q.get('options')
                    
                    if not correct or not options or not isinstance(options, list):
                        continue
                        
                    # Logic: is correct answer strictly longest?
                    sorted_opts = sorted(options, key=len, reverse=True)
                    if sorted_opts[0] == correct and len(options) > 1 and len(sorted_opts[0]) > len(sorted_opts[1]):
                        all_problems.append({
                            'file': fpath,
                            'question': q_text,
                            'correct': correct,
                            'options': options,
                            'diff': len(sorted_opts[0]) - len(sorted_opts[1])
                        })

            except Exception as e:
                print(f"Skipping {fpath}: {e}")

    # Sort by length difference (most obvious first)
    all_problems.sort(key=lambda x: x['diff'], reverse=True)
    
    print(f"Total unique questions with length bias: {len(all_problems)}")
    
    # Save to a file for me to read
    with open('biased_questions_list.json', 'w') as f:
        json.dump(all_problems, f, indent=2)

if __name__ == '__main__':
    analyze()
