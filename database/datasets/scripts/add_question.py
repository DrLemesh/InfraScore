import json
import os
import subprocess
import sys

# Path to the dataset relative to this script
DATASET_REL_PATH = "../final_quiz_dataset.json"

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.normpath(os.path.join(script_dir, DATASET_REL_PATH))
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset file not found at {dataset_path}")
        print("Please run this script from the scripts directory.")
        return

    print("==========================================")
    print("   Add New Question to InfraScore DB")
    print("==========================================")
    
    # 1. Gather Details
    category = input("Category (e.g. Docker, Kubernetes): ").strip()
    while not category:
        category = input("Category is required: ").strip()
        
    question_text = input("Question Text: ").strip()
    while not question_text:
        question_text = input("Question text is required: ").strip()
    
    # 2. Options
    print("\nEnter Options (Press Enter without typing to finish, min 2 options):")
    options = []
    while True:
        opt = input(f"Option {len(options)+1}: ").strip()
        if not opt:
            if len(options) < 2:
                print("Error: You need at least 2 options.")
                continue
            break
        options.append(opt)
        
    # 3. Correct Answer
    print("\nSelect the Correct Answer:")
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")
        
    correct_idx = -1
    while True:
        try:
            choice = input(f"Enter number (1-{len(options)}): ").strip()
            val = int(choice)
            if 1 <= val <= len(options):
                correct_idx = val - 1
                break
        except ValueError:
            pass
        print("Invalid selection.")
        
    correct_answer = options[correct_idx]
    
    # 4. Difficulty
    difficulty = 3
    try:
        diff_in = input("Difficulty (1=Junior, 3=Mid, 5=Senior) [Default: 3]: ").strip()
        if diff_in:
            difficulty = int(diff_in)
    except:
        print("Invalid difficulty, defaulting to 3.")

    # 5. Construct Object
    new_q = {
        "category": category,
        "type": "multiple_choice",
        "difficulty": difficulty,
        "question": question_text,
        "correct_answer": correct_answer,
        "options": options,
        "metadata": {
            "estimated_minutes": 1,
            "tags": [category]
        }
    }
    
    # 6. Load & Save
    try:
        with open(dataset_path, 'r') as f:
            data = json.load(f)
            
        # Assign ID
        new_id = 1
        if data:
            new_id = max([item.get('id', 0) for item in data]) + 1
        new_q['id'] = new_id
        
        data.append(new_q)
        
        with open(dataset_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"\n✅ Question added successfully! New ID: {new_id}")
        print(f"Total questions: {len(data)}")
        
    except Exception as e:
        print(f"Error saving file: {e}")
        return

    # 7. Sync
    print("\n------------------------------------------")
    print("To make this question available in the app, we need to update the database.")
    do_sync = input("Do you want to update the running database NOW? (y/n): ").lower()
    
    if do_sync == 'y':
        print("\n[1/2] Copying dataset to container...")
        try:
            subprocess.run(
                f"docker cp {dataset_path} devops_quiz_app:/app/final_quiz_dataset.json", 
                shell=True, check=True
            )
            
            print("[2/2] Reseeding database (this takes a moment)...")
            subprocess.run(
                "docker exec devops_quiz_app python /app/seed_db.py", 
                shell=True, check=True
            )
            print("\n🎉 Success! The new question is live.")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error during sync: {e}")
            print("You may need to run 'docker cp' and 'docker exec' manually.")
    else:
        print("\nOkay. Remember to run the update manually later.")
