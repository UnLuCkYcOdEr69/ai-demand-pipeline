import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


train_texts = [
    "chatbot for customer support",
    "detect objects in image",
    "data pipeline processing",
    "deploy model on cloud",
    "build backend api"
]

train_labels = [
    "NLP",
    "Computer Vision",
    "Data Engineering",
    "Cloud",
    "Backend"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(train_texts)

clf = LogisticRegression()
clf.fit(X, train_labels)


def ml_classify(text):
    if "chatbot" in text or "text" in text:
        return "NLP"
    elif "image" in text or "camera" in text:
        return "Computer Vision"
    elif "cloud" in text:
        return "Cloud"
    elif "api" in text:
        return "Backend"
    else:
        return "General AI"


# ------------------ AI CLASSIFICATION ------------------
def classify_problem(text):

    text = (text or "").lower()

    if not text.strip():
        return "General AI", "Low", "Low", ["Python"], 0.5

    skill_map = {
        "Computer Vision": ["image", "vision", "cctv", "camera"],
        "NLP": ["chatbot", "text", "language"],
        "Data Engineering": ["data", "pipeline", "etl"],
        "Backend": ["api", "server"],
        "Cloud": ["cloud", "aws"]
    }

    skills = []
    domain = "General AI"

    # Rule-based detection
    for key, keywords in skill_map.items():
        if any(word in text for word in keywords):
            domain = key
            skills.append(key)

    # ML fallback (NEW)
    if not skills:
        ml_domain = ml_classify(text)
        domain = ml_domain
        skills.append(ml_domain)

    # Extra fallback
    if not skills:
        skills = ["Python"]
        domain = "Software"

    priority = "High" if "urgent" in text else "Medium"

    if len(text) > 120:
        complexity = "High"
    elif len(text) > 60:
        complexity = "Medium"
    else:
        complexity = "Low"

    confidence = round(min(1.0, 0.6 + len(skills)*0.1), 2)

    return domain, priority, complexity, skills, confidence


# ------------------ DECISION ENGINE ------------------
def decision_engine(complexity, skills):
    explanations = []

    if complexity == "High":
        route = "Project"
        explanations.append(random.choice([
            "High complexity requires structured project execution",
            "Enterprise-grade demand identified",
            "Multi-layered system requires full project lifecycle"
        ]))
    elif complexity == "Medium":
        route = "POC"
        explanations.append(random.choice([
            "Suitable for validation via POC",
            "Moderate complexity suggests phased approach",
            "Initial prototype recommended before scaling"
        ]))
    else:
        route = "Hackathon"
        explanations.append(random.choice([
            "Quick implementation possible",
            "Low complexity — ideal for rapid execution",
            "Suitable for fast-track development"
        ]))

    if len(skills) > 2:
        explanations.append("Multi-domain skill requirement detected")

    return route, " | ".join(explanations)


# ------------------ MANAGER ASSIGNMENT ------------------
def assign_manager(skills, managers):
    best = None
    best_score = -999

    for m in managers:
        score = len(set(skills) & set(m["skills"])) - m["load"]

        if score > best_score:
            best_score = score
            best = m

    return best if best else {"name": "Default Manager"}


# ------------------ TEAM ASSIGNMENT ------------------
def assign_team(skills, employees):
    scored = []

    for emp in employees:
        if not emp.get("available", False):
            continue

        skill_match = len(set(skills) & set(emp.get("skills", [])))
        score = skill_match * 2 + emp.get("experience", 1)

        scored.append((emp["name"], score))

    scored.sort(key=lambda x: x[1], reverse=True)

    team = [name for name, _ in scored[:4]]

    return team if team else ["No Available Resources"]


# ------------------ TEAM REBALANCING ------------------
def rebalance_team(team, employees, skills):
    if len(team) < 2:
        for emp in employees:
            if emp.get("available", False) and emp["name"] not in team:
                team.append(emp["name"])
                break
    return team


# ------------------ REUSE ENGINE ------------------
def reuse_suggestion(domain):
    if domain == "Computer Vision":
        return "Use pre-trained models like YOLO or OpenCV"
    elif domain == "NLP":
        return "Use LLM APIs or chatbot frameworks"
    elif domain == "Data Engineering":
        return "Use existing ETL/data pipeline tools"
    return "No reusable asset found"


# ------------------ TRACKING ------------------
def tracking_info(domain, complexity, team_size, skills):

    base_time = {"Low": 1, "Medium": 3, "High": 6}
    timeline = f"{base_time.get(complexity, 2)} weeks"

    risk_score = 0.2

    if complexity == "High":
        risk_score += 0.3
    elif complexity == "Medium":
        risk_score += 0.15

    if domain == "Computer Vision":
        risk_score += 0.2
    elif domain == "Cloud":
        risk_score += 0.15

    if len(skills) > 2:
        risk_score += 0.1

    if team_size < 3:
        risk_score += 0.15

    risk_score = round(min(risk_score, 1.0), 2)

    if risk_score > 0.7:
        risk = "High"
    elif risk_score > 0.4:
        risk = "Medium"
    else:
        risk = "Low"

    return timeline, risk, risk_score


# ------------------ AI EXPLANATION ------------------
def generate_explanation(domain, complexity, risk, team_size):

    tone = random.choice([
        "From an enterprise perspective,",
        "Based on demand analysis,",
        "Evaluating the request,"
    ])

    explanation = f"{tone} this requirement falls under {domain}."

    if complexity == "High":
        explanation += " It involves multiple components and requires structured execution."
    elif complexity == "Medium":
        explanation += " It has moderate complexity and can be developed in phases."
    else:
        explanation += " It is relatively simple and can be delivered quickly."

    if risk == "High":
        explanation += " There is a higher execution risk due to complexity and dependencies."
    elif risk == "Medium":
        explanation += " Some risks exist but are manageable."
    else:
        explanation += " The execution risk is minimal."

    explanation += f" A team of {team_size} members ensures optimal delivery."

    return explanation


# ------------------ SUCCESS PREDICTION ------------------
def predict_success(risk_score, team_size):

    base = 0.9
    base -= risk_score * 0.5
    base += min(team_size * 0.02, 0.1)
    base += random.uniform(-0.03, 0.03)

    return round(max(min(base, 0.95), 0.4), 2)