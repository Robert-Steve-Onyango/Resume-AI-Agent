import os
import random
import re
import time
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

try:
    import PyPDF2
except ImportError:  # pragma: no cover - import guard
    PyPDF2 = None

try:
    import docx
except ImportError:  # pragma: no cover - import guard
    docx = None

try:
    import spacy
except ImportError:  # pragma: no cover - import guard
    spacy = None

BASE_DIR = Path(__file__).resolve().parent
LEADERBOARD_FILE = BASE_DIR / "leaderboard.txt"

nlp = None


def load_nlp():
    global nlp
    if spacy is None:
        nlp = None
        return nlp

    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        try:
            nlp = spacy.blank("en")
        except Exception:  # pragma: no cover - fallback guard
            nlp = None
    return nlp


load_nlp()


# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    if PyPDF2 is None:
        raise RuntimeError("PyPDF2 is not installed. Run: pip install -r requirements.txt")

    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text


# Function to extract text from DOCX
def extract_text_from_docx(file_path):
    if docx is None:
        raise RuntimeError("python-docx is not installed. Run: pip install -r requirements.txt")

    document = docx.Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text


# Function to check for key sections
def check_sections(text):
    sections = ["Education", "Experience", "Skills", "Projects"]
    found_sections = []
    for section in sections:
        if re.search(rf"\b{section}\b", text, re.IGNORECASE):
            found_sections.append(section)
    return found_sections


# Function to analyze grammar and spelling
def analyze_grammar(text):
    if not text or not text.strip():
        return []

    errors = []
    if nlp is None:
        if re.search(r"\bwas\b|\bwere\b", text, re.IGNORECASE):
            errors.append("Passive voice detected")
        return errors

    doc = nlp(text)
    for sent in doc.sents:
        if not sent.text.strip():
            continue
        if "was" in sent.text or "were" in sent.text:
            errors.append(f"Passive voice detected: {sent.text}")
    return errors


# Function to rate the CV
def rate_cv(text):
    score = 10
    sections = check_sections(text)
    if len(sections) < 3:  # Missing key sections
        score -= 3
    grammar_errors = analyze_grammar(text)
    if grammar_errors:
        score -= 2
    return max(1, min(10, score))  # Ensure score is between 1 and 10


# Function to generate a fun rating
def get_fun_rating(score):
    if score == 10:
        return "CV Masterpiece! 🎨"
    if 7 <= score < 10:
        return "Almost Perfect! ✨"
    if 4 <= score < 7:
        return "Good, but needs work! 🛠"
    return "Let's start from scratch! 🚀"


# Function to generate feedback
def generate_feedback(text):
    feedback = []
    sections = check_sections(text)
    missing_sections = set(["Education", "Experience", "Skills", "Projects"]) - set(sections)
    if missing_sections:
        feedback.append(f"Missing sections: {', '.join(missing_sections)}")
    grammar_errors = analyze_grammar(text)
    if grammar_errors:
        feedback.append("Grammar issues detected. Consider revising.")
    return "\n".join(feedback) if feedback else "Your CV looks great! No major issues found."


# Function to get a random tip
def get_random_tip():
    tips = [
        "Use action verbs like 'managed', 'developed', and 'achieved'.",
        "Keep your CV to 1-2 pages.",
        "Tailor your CV to the job description.",
        "Proofread your CV for spelling and grammar errors.",
    ]
    return random.choice(tips)


# Function to save the score to a leaderboard
def save_score(name, score):
    with LEADERBOARD_FILE.open("a", encoding="utf-8") as file:
        file.write(f"{name}: {score}\n")


# Function to show the leaderboard
def show_leaderboard():
    try:
        with LEADERBOARD_FILE.open("r", encoding="utf-8") as file:
            scores = file.readlines()
        leaderboard = "Leaderboard:\n" + "".join(scores)
        messagebox.showinfo("Leaderboard", leaderboard)
    except FileNotFoundError:
        messagebox.showinfo("Leaderboard", "No scores yet!")


# Function to handle file upload
def upload_file():
    file_path = filedialog.askopenfilename(
        title="Upload your CV",
        filetypes=[("PDF Files", ".pdf"), ("Word Documents", ".docx")],
    )
    if not file_path:
        return

    progress_bar.start(10)  # Start the progress bar
    root.update_idletasks()  # Update the GUI
    try:
        if file_path.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file_path.endswith(".docx"):
            text = extract_text_from_docx(file_path)
        else:
            messagebox.showerror("Error", "Unsupported file format!")
            return

        score = rate_cv(text)
        fun_rating = get_fun_rating(score)
        feedback = generate_feedback(text)
        tip = get_random_tip()
        emoji = "🎉" if score >= 8 else "😐" if 5 <= score < 8 else "😢"

        # Save score and show results
        name = simpledialog.askstring("Name", "Enter your name to save your score:")
        if name:
            save_score(name, score)
        messagebox.showinfo(
            "CV Rating",
            f"🤖 says: Your CV score is: {score}/10 {emoji}\n{fun_rating}\n\nFeedback:\n{feedback}\n\nTip: {tip}",
        )
        show_leaderboard()

        # Ask if the user wants to try again
        retry = messagebox.askyesno("Try Again", "Do you want to upload a revised CV?")
        if retry:
            upload_file()
    except Exception as exc:
        messagebox.showerror("Error", f"An error occurred: {exc}")
    finally:
        progress_bar.stop()  # Stop the progress bar


# Function to start the timer
def start_timer():
    def _countdown():
        for i in range(300, -1, -1):
            mins, secs = divmod(i, 60)
            timer_label.config(text=f"Time left: {mins:02}:{secs:02}")
            root.update()
            time.sleep(1)
        messagebox.showinfo("Time's up!", "Time's up! How did you do?")

    import threading

    threading.Thread(target=_countdown, daemon=True).start()


# Create the Tkinter GUI
def build_ui():
    global root, label, progress_bar, upload_button, timer_label, start_button

    root = tk.Tk()
    root.title("CV Rating AI 🤖")
    root.geometry("500x300")

    # Add a label
    label = tk.Label(root, text="Upload your CV to get a rating!", font=("Arial", 16))
    label.pack(pady=20)

    # Add a progress bar
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="indeterminate")
    progress_bar.pack(pady=10)

    # Add an upload button
    upload_button = tk.Button(root, text="Upload CV", command=upload_file, font=("Arial", 14))
    upload_button.pack(pady=10)

    # Add a timer label
    timer_label = tk.Label(root, text="Time left: 05:00", font=("Arial", 12))
    timer_label.pack(pady=10)

    # Add a start timer button
    start_button = tk.Button(root, text="Start Timer", command=start_timer, font=("Arial", 12))
    start_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    build_ui() 