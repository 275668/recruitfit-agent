from __future__ import annotations


QUESTION_TEMPLATES = {
    "Product Requirement Document": {
        "main": "Walk through a PRD you owned. What problem did it define, and how did it guide execution?",
        "follow_up": "What tradeoffs or requirement changes did you manage after stakeholder feedback?",
        "focus": "Problem framing, requirement clarity, tradeoff handling, execution support.",
    },
    "User Story": {
        "main": "Describe a user story you wrote that changed the product team's implementation approach.",
        "follow_up": "How did you define acceptance criteria and validate that the story was complete?",
        "focus": "User-centered thinking, acceptance criteria, delivery clarity.",
    },
    "Prototype Design": {
        "main": "Tell me about a prototype you created or reviewed before development started.",
        "follow_up": "What did the prototype help the team learn or decide?",
        "focus": "Product visualization, user feedback, design-to-build translation.",
    },
    "AI Agent": {
        "main": "Describe an AI agent workflow you designed, built, or evaluated.",
        "follow_up": "How did you define the agent stages, failure handling, and human review points?",
        "focus": "Agent workflow understanding, control boundaries, practical implementation.",
    },
    "LLM": {
        "main": "Give an example of work where you used or evaluated a large language model.",
        "follow_up": "How did you judge output quality and reduce unsupported assumptions?",
        "focus": "LLM literacy, quality judgment, hallucination awareness.",
    },
    "Prompt Engineering": {
        "main": "Share a prompt design example where changing the prompt improved output quality.",
        "follow_up": "What variables did you test, and how did you evaluate the improvement?",
        "focus": "Prompt iteration, evaluation discipline, clarity of constraints.",
    },
    "RAG": {
        "main": "Describe your experience with retrieval augmented generation or retrieval-based workflows.",
        "follow_up": "How did you decide what source content should be retrieved and cited?",
        "focus": "Retrieval design, grounding, source quality.",
    },
    "Workflow Design": {
        "main": "Walk through a multi-stage workflow or pipeline you designed.",
        "follow_up": "Where did you add checks, handoffs, or error handling?",
        "focus": "Process decomposition, sequencing, reliability.",
    },
    "Python": {
        "main": "Describe a Python project or analysis workflow you personally implemented.",
        "follow_up": "Which libraries did you use, and what parts did you structure into reusable code?",
        "focus": "Hands-on coding, code structure, practical tooling.",
    },
    "Streamlit": {
        "main": "Tell me about a Streamlit app or internal demo you built.",
        "follow_up": "How did users interact with it, and what feedback changed the design?",
        "focus": "Demo implementation, user workflow, interface thinking.",
    },
    "SQL": {
        "main": "Describe a SQL analysis you wrote to answer a business question.",
        "follow_up": "How did you validate the query result and handle messy data?",
        "focus": "Query skill, data validation, business interpretation.",
    },
    "Data Analysis": {
        "main": "Give an example of an analysis that changed a product or business decision.",
        "follow_up": "What data did you use, and how did you communicate uncertainty?",
        "focus": "Analytical reasoning, decision impact, communication.",
    },
    "A/B Testing": {
        "main": "Walk through an A/B test you designed, analyzed, or interpreted.",
        "follow_up": "How did you choose the metric, sample, and decision rule?",
        "focus": "Experiment design, metric choice, causal interpretation.",
    },
    "Evaluation Metrics": {
        "main": "Describe a metric framework you created for a product, model, or workflow.",
        "follow_up": "How did you prevent the metric from encouraging the wrong behavior?",
        "focus": "Metric design, tradeoffs, product judgment.",
    },
    "Cross-functional Communication": {
        "main": "Tell me about a time you aligned stakeholders with different priorities.",
        "follow_up": "What did you communicate differently to technical and non-technical partners?",
        "focus": "Stakeholder management, clarity, influence.",
    },
    "Hiring and Interview": {
        "main": "Describe your experience designing or supporting a hiring interview process.",
        "follow_up": "How did you make the process structured and fair for candidates?",
        "focus": "Interview structure, evidence-based evaluation, fairness.",
    },
    "HR Tech": {
        "main": "What HR tech or recruiting workflow have you worked with or studied closely?",
        "follow_up": "Where do you see the main risks in applying AI to recruiting workflows?",
        "focus": "Domain understanding, practical constraints, responsible AI awareness.",
    },
}


def generate_interview_questions(risk_items: list[dict]) -> list[dict]:
    """Generate targeted interview questions for missing or weak evidence."""
    questions = []

    for risk in risk_items:
        template = QUESTION_TEMPLATES.get(
            risk["skill_name"],
            {
                "main": f"Describe a concrete project where you used {risk['skill_name']}.",
                "follow_up": "What was your role, what decisions did you make, and what was the outcome?",
                "focus": "Specific evidence, personal ownership, measurable impact.",
            },
        )

        questions.append(
            {
                "skill_name": risk["skill_name"],
                "main_question": template["main"],
                "follow_up_question": template["follow_up"],
                "evaluation_focus": template["focus"],
            }
        )

    return questions
