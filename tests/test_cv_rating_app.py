import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import cv_rating_app


def test_check_sections_detects_known_sections():
    text = "Education\nExperience\nSkills\nProjects"
    assert cv_rating_app.check_sections(text) == ["Education", "Experience", "Skills", "Projects"]


def test_rate_cv_returns_score_within_range():
    text = "Education\nExperience\nSkills\nProjects"
    score = cv_rating_app.rate_cv(text)
    assert 1 <= score <= 10


def test_generate_feedback_handles_missing_sections():
    text = "Experience\nSkills"
    feedback = cv_rating_app.generate_feedback(text)
    assert "Missing sections" in feedback
