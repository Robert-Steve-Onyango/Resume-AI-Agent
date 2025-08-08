from ai_engine import analyze_resume_text
from flask import Flask, request, render_template, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import PyPDF2
import psycopg2

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path)


app = Flask(__name__)

# Route to handle PDF upload and extract text without saving the file
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/extract_text', methods=['POST'])
def extract_text_route():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    # Use the file stream directly
    
    def extract_text(file_obj):
        text = ""
        reader = PyPDF2.PdfReader(file_obj)
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    text = extract_text(file)
    return jsonify({'text': text})

# Route to save user credentials and resume text
@app.route('/save_resume', methods=['POST'])
def save_resume():
    import sys
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    content = data.get('content')
    print(f"Received: name={name}, email={email}, content_length={len(content) if content else 0}", file=sys.stderr)
    if not name or not email or not content:
        print("Missing required fields", file=sys.stderr)
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432')
        )
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO resumes (name, email, content)
            VALUES (%s, %s, %s)
        ''', (name, email, content))
        conn.commit()
        cursor.close()
        conn.close()
        print("Resume saved successfully", file=sys.stderr)
        return jsonify({'message': 'Resume saved successfully'})
    except Exception as e:
        print(f"Database error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

# Agent route for resume analysis
@app.route('/resume_agent', methods=['POST'])
def resume_agent():
    data = request.get_json()
    resume_text = data.get('content')
    if not resume_text:
        return jsonify({'error': 'No resume text provided'}), 400
    # Prompts for each task
    summary_prompt = "Summarize this resume in 20 words."
    roles_prompt = "List 3 job roles this candidate is a match for, based on the resume."
    insight_prompt = "Give a career insight (next step) for this candidate in 20 words."
    keywords_prompt = "List 10 keywords to include in this resume."

    summary = analyze_resume_text(resume_text, summary_prompt)
    roles = analyze_resume_text(resume_text, roles_prompt)
    insight = analyze_resume_text(resume_text, insight_prompt)
    keywords = analyze_resume_text(resume_text, keywords_prompt)

    # Try to split roles and keywords into lists
    roles_list = [r.strip() for r in roles.split('\n') if r.strip()][:3]
    keywords_list = [k.strip() for k in keywords.replace(',', '\n').split('\n') if k.strip()][:10]

    return jsonify({
        'summary': summary,
        'roles': roles_list,
        'career_insight': insight,
        'keywords': keywords_list
    })
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)

