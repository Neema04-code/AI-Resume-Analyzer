def analyze_resume(text):

    text_lower = text.lower()

    skills = [
        "python",
        "java",
        "c++",
        "c#",
        "html",
        "css",
        "javascript",
        "sql",
        "git",
        "github",
        "aws",
        "cloud"
    ]

    found_skills = []
    missing_skills = []

    for skill in skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)


    # Score calculation
    score = 0


    # Skills score (50 marks)
    skill_score = (len(found_skills) / len(skills)) * 50
    score += skill_score


    # Education score (20 marks)
    if "bca" in text_lower or "b.tech" in text_lower or "degree" in text_lower:
        score += 20


    # Project score (15 marks)
    if "project" in text_lower or "projects" in text_lower:
        score += 15


    # Certification score (10 marks)
    if "certificate" in text_lower or "certification" in text_lower:
        score += 10


    # Experience score (5 marks)
    if "internship" in text_lower or "experience" in text_lower:
        score += 5


    score = int(score)


    return {
        "score": score,
        "found": found_skills,
        "missing": missing_skills
    }