import os
import tempfile
import time
from pathlib import Path

import streamlit as st

from cv_rating_app import (
    extract_text_from_docx,
    extract_text_from_pdf,
    generate_feedback,
    get_fun_rating,
    get_random_tip,
    rate_cv,
    save_score,
)

BASE_DIR = Path(__file__).resolve().parent
LEADERBOARD_FILE = BASE_DIR / "leaderboard.txt"


def show_leaderboard():
    if LEADERBOARD_FILE.exists():
        with LEADERBOARD_FILE.open("r", encoding="utf-8") as file:
            scores = file.readlines()
        st.info("Leaderboard:\n" + "".join(scores))
    else:
        st.info("Leaderboard:\nNo scores yet!")


def extract_text_from_uploaded_file(uploaded_file):
    suffix = Path(uploaded_file.name).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_path = temp_file.name

    try:
        if suffix == ".pdf":
            return extract_text_from_pdf(temp_path)
        if suffix == ".docx":
            return extract_text_from_docx(temp_path)
        raise ValueError("Unsupported file format")
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


st.title("CV Rating AI 🤖")
st.write("Upload your CV to get a rating!")

uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner("Processing your CV..."):
        try:
            text = extract_text_from_uploaded_file(uploaded_file)
        except Exception as exc:
            st.error(f"Could not read the file: {exc}")
            st.stop()

        score = rate_cv(text)
        fun_rating = get_fun_rating(score)
        feedback = generate_feedback(text)
        tip = get_random_tip()
        emoji = "🎉" if score >= 8 else "😐" if 5 <= score < 8 else "😢"

        st.success(f"🤖 says: Your CV score is: {score}/10 {emoji}")
        st.info(fun_rating)
        st.write("**Feedback:**")
        st.write(feedback)
        st.write(f"**Tip:** {tip}")

        name = st.text_input("Enter your name to save your score:")
        if name and st.button("Save Score"):
            save_score(name, score)
            st.success("Score saved!")
            show_leaderboard()

    if st.button("Show Leaderboard"):
        show_leaderboard()

    if st.button("Start 5-Minute Timer"):
        st.session_state["timer_start"] = time.time()

    if "timer_start" in st.session_state:
        elapsed = int(time.time() - st.session_state["timer_start"])
        remaining = max(0, 300 - elapsed)
        mins, secs = divmod(remaining, 60)
        st.write(f"Time left: {mins:02}:{secs:02}")
        if remaining == 0:
            st.warning("Time's up! How did you do?")