from flask import Flask, render_template, request

from model import (
    classify_problem,
    decision_engine,
    assign_manager,
    assign_team,
    rebalance_team,
    reuse_suggestion,
    tracking_info,
    generate_explanation,   
    predict_success   
)

from data import managers, employees

app = Flask(__name__)

# ------------------ HOME ------------------
@app.route("/")
def home():
    return render_template("index.html")


# ------------------ PROCESS ------------------
@app.route("/process", methods=["POST"])
def process():

    problem = request.form.get("problem")

    if not problem:
        return render_template("index.html", error="Please enter a problem statement")

    # Step 1: Classification
    domain, priority, complexity, skills, confidence = classify_problem(problem)

    # Step 2: Decision
    route, reason = decision_engine(complexity, skills)

    # Step 3: Manager Assignment
    manager = assign_manager(skills, managers)
    manager_name = manager.get("name", "Default Manager")

    # Step 4: Team Allocation
    team = assign_team(skills, employees)

    # Step 5: Rebalancing
    team = rebalance_team(team, employees, skills)

    # Step 6: Reuse Suggestion
    reuse = reuse_suggestion(domain)

    # Step 7: Tracking
    timeline, risk, risk_score = tracking_info(
        domain,
        complexity,
        len(team),
        skills
    )
    # AI Explanation
    ai_explanation = generate_explanation(domain, complexity, risk, len(team))

    # Success prediction
    success_rate = predict_success(risk_score, len(team))

    # Step 8: Automation Impact
    import random

    manual_before = random.choice([5, 6, 7])

    if complexity == "High":
        manual_after = random.choice([2, 3])
    elif complexity == "Medium":
        manual_after = random.choice([1, 2])
    else:
        manual_after = 1
        
    time_saved_percent = int(((manual_before - manual_after) / manual_before) * 100)

    automation_gain = {
        "manual_steps_before": manual_before,
        "manual_steps_after": manual_after,
        "time_saved": f"{time_saved_percent}%"
    }
    
    return render_template(
        "result.html",
        problem=problem,
        domain=domain,
        priority=priority,
        complexity=complexity,
        skills=skills,
        route=route,
        reason=reason,
        manager=manager_name,
        team=team,
        reuse=reuse,
        timeline=timeline,
        risk=risk,
        confidence=confidence,
        risk_score=risk_score,
        automation=automation_gain,
        ai_explanation=ai_explanation,
        success_rate=success_rate
        
    )


# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(debug=True)