from flask import Flask, request, render_template, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
from parsing import extract_text
from ai_engine import analyze_resume, fetch_job_boards

# Configuration
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path)

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Helpers
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return redirect(request.url)
    file = request.files['resume']
    if file.filename == '' or not allowed_file(file.filename):
        return redirect(request.url)
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file.save(filepath)

    # Extract text
    text = extract_text(filepath)
    # Analyze with AI
    profile = analyze_resume(text)
    # Fetch job board data
    jobs = fetch_job_boards(profile['skills'])

    return render_template('results.html', profile=profile, jobs=jobs)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.get_json()
    text = data.get('text', '')
    profile = analyze_resume(text)
    jobs = fetch_job_boards(profile['skills'])
    return jsonify({**profile, 'jobs': jobs})

@app.route('/job-finder')
@app.route('/scroll-jobs')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)