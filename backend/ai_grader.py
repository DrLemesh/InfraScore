
import os
import json
import google.generativeai as genai

def evaluate_answer(question_text, user_answer, reference_answer):
    """
    Evaluates a user's answer against a reference answer using Gemini API.
    
    Returns:
        dict: {
            "score": int (1-10),
            "feedback": str (explanation of the score and what was missing/good),
            "is_correct": bool (derived from score >= 7)
        }
    """
    api_key = os.environ.get('GEMINI_API_KEY')
    
    if not api_key:
        print("Warning: GEMINI_API_KEY not found. Skipping AI grading.")
        return {
            "score": 0,
            "feedback": "AI grading unavailable (API Key missing).",
            "is_correct": False,
            "error": "missing_key"
        }

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-lite-preview-02-05')
        
        prompt = f"""
        You are an expert DevOps instructor grading a student's answer.
        
        Question: {question_text}
        
        Reference/Correct Answer: {reference_answer}
        
        Student's Answer: {user_answer}
        
        Task:
        1. Compare the student's answer to the reference answer.
        2. Rate the answer on a scale of 1 to 10 based on accuracy and completeness (10 being perfect).
        3. Provide concise feedback (max 2 sentences) explaining the rating. Mention what they got right or missed.
        
        Output Format (strictly JSON):
        {{
            "score": <int>,
            "feedback": "<string>"
        }}
        """
        
        response = model.generate_content(prompt)
        result_text = response.text.replace('```json', '').replace('```', '').strip()
        
        result_json = json.loads(result_text)
        
        score = result_json.get('score', 0)
        feedback = result_json.get('feedback', 'No feedback provided.')
        
        # Determine pass/fail based on score threshold
        is_correct = score >= 7
        
        return {
            "score": score,
            "feedback": feedback,
            "is_correct": is_correct
        }
        
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return {
            "score": 0,
            "feedback": "Error evaluating answer. Please try again later.",
            "is_correct": False,
            "error": str(e)
        }
