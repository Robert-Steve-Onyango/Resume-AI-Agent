# CV Rating AI 🤖

A fun and interactive CV rating application that analyzes your CV and provides feedback, tips, and a score.

## Features

- Upload PDF or DOCX CV files
- Automatic analysis of key sections (Education, Experience, Skills, Projects)
- Grammar and passive voice detection
- Fun rating system with emojis
- Random CV tips
- Leaderboard system
- 5-minute timer for CV review sessions

## Requirements

- Python 3.7 or higher
- Required packages listed in `requirements.txt`

## Installation

1. Create a Python 3.11 environment (this project works best with Python 3.11):
   ```bash
   py -3.11 -m venv .venv311
   ```
2. Activate it and install the required packages:
   ```bash
   .venv311\Scripts\activate
   pip install -r requirements.txt
   ```
3. If you prefer a simpler launch on Windows, run:
   ```bat
   run_app.bat
   ```

## Usage

1. Run the application:
   ```bash
   .venv311\Scripts\python.exe cv_rating_app.py
   ```
2. Click the "Upload CV" button to select your CV file (PDF or DOCX)
3. Enter your name when prompted to save your score
4. View your CV rating, feedback, and tips
5. Check the leaderboard to see how you compare to others
6. Use the timer feature to set a 5-minute review session

## How it Works

The application analyzes your CV for:
- Presence of key sections (Education, Experience, Skills, Projects)
- Grammar and passive voice usage
- Overall structure and completeness

Based on the analysis, it provides:
- A score out of 10
- Fun rating with emojis
- Specific feedback on missing sections or issues
- Random tips for improvement
- A leaderboard to track your progress

## Note

This is a fun tool to help you improve your CV. While it provides useful feedback, it's recommended to also have your CV reviewed by professionals or mentors for the best results. 