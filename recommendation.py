def get_recommendations(found_skills, missing_skills):

    suggestions = []
    jobs = []

    # Suggestions
    if "Python" in found_skills:
        suggestions.append("Improve Python skills with projects and advanced concepts.")
    else:
        suggestions.append("Learn Python programming.")

    if "SQL" not in found_skills:
        suggestions.append("Learn SQL and database management.")

    if "Git" not in found_skills:
        suggestions.append("Learn Git and GitHub for software development.")

    if len(found_skills) < 5:
        suggestions.append("Add more technical skills and projects to your resume.")

    # Job recommendations
    if "Python" in found_skills and "SQL" in found_skills:
        jobs.append("Python Developer")
        jobs.append("Backend Developer")

    if "HTML" in found_skills:
        jobs.append("Web Developer")

    if "Java" in found_skills:
        jobs.append("Java Developer")

    if not jobs:
        jobs.append("Software Engineer Intern")

    return suggestions, jobs