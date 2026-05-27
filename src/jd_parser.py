from __future__ import annotations


SKILL_DICTIONARY = [
    {
        "skill_name": "Product Requirement Document",
        "skill_category": "Product Management",
        "required_keywords": ["prd", "prds", "product requirement", "product requirements", "requirements document"],
        "importance": "High",
    },
    {
        "skill_name": "User Story",
        "skill_category": "Product Management",
        "required_keywords": ["user story", "user stories", "acceptance criteria"],
        "importance": "Medium",
    },
    {
        "skill_name": "Prototype Design",
        "skill_category": "Product Management",
        "required_keywords": ["prototype", "wireframe", "figma", "mockup"],
        "importance": "Medium",
    },
    {
        "skill_name": "AI Agent",
        "skill_category": "AI and LLM",
        "required_keywords": [
            "agent",
            "agent system",
            "agent workflow",
            "ticket agent",
            "ai agent",
            "agentic",
            "autonomous agent",
        ],
        "importance": "High",
    },
    {
        "skill_name": "LLM",
        "skill_category": "AI and LLM",
        "required_keywords": ["llm", "large language model", "gpt", "language model"],
        "importance": "High",
    },
    {
        "skill_name": "Prompt Engineering",
        "skill_category": "AI and LLM",
        "required_keywords": ["prompt", "prompt engineering", "prompt design"],
        "importance": "High",
    },
    {
        "skill_name": "RAG",
        "skill_category": "AI and LLM",
        "required_keywords": ["rag", "retrieval augmented generation", "retrieval"],
        "importance": "Medium",
    },
    {
        "skill_name": "Workflow Design",
        "skill_category": "Agent Workflow",
        "required_keywords": ["workflow", "multi-stage", "pipeline", "orchestration"],
        "importance": "High",
    },
    {
        "skill_name": "Python",
        "skill_category": "Technical Tools",
        "required_keywords": ["python", "pandas", "numpy"],
        "importance": "Medium",
    },
    {
        "skill_name": "Streamlit",
        "skill_category": "Technical Tools",
        "required_keywords": ["streamlit"],
        "importance": "Medium",
    },
    {
        "skill_name": "SQL",
        "skill_category": "Technical Tools",
        "required_keywords": ["sql", "database", "query"],
        "importance": "Medium",
    },
    {
        "skill_name": "Data Analysis",
        "skill_category": "Data Analysis",
        "required_keywords": [
            "data analysis",
            "growth analysis",
            "analytics",
            "insight",
            "dashboard",
            "dashboards",
            "product dashboards",
        ],
        "importance": "High",
    },
    {
        "skill_name": "A/B Testing",
        "skill_category": "Experiment Design",
        "required_keywords": ["a/b testing", "ab testing", "experiment", "controlled test"],
        "importance": "Medium",
    },
    {
        "skill_name": "Evaluation Metrics",
        "skill_category": "Experiment Design",
        "required_keywords": ["metrics", "evaluation metric", "kpi", "success metric"],
        "importance": "High",
    },
    {
        "skill_name": "Cross-functional Communication",
        "skill_category": "Communication",
        "required_keywords": [
            "cross-functional",
            "stakeholder",
            "stakeholders",
            "communicate",
            "communicated",
            "communication",
            "collaborate",
            "collaborated",
            "presented",
        ],
        "importance": "High",
    },
    {
        "skill_name": "Hiring and Interview",
        "skill_category": "Domain Knowledge",
        "required_keywords": ["hiring", "interview", "screening", "candidate"],
        "importance": "High",
    },
    {
        "skill_name": "HR Tech",
        "skill_category": "Domain Knowledge",
        "required_keywords": ["hr tech", "recruiting", "recruitment", "talent acquisition"],
        "importance": "Medium",
    },
]


def parse_jd_requirements(jd_text: str) -> list[dict]:
    """Extract JD requirements with a transparent keyword dictionary."""
    normalized_jd = jd_text.lower()
    requirements = []

    for skill in SKILL_DICTIONARY:
        matched_keywords = [
            keyword for keyword in skill["required_keywords"] if keyword in normalized_jd
        ]
        if matched_keywords:
            requirements.append(
                {
                    "skill_name": skill["skill_name"],
                    "skill_category": skill["skill_category"],
                    "required_keywords": skill["required_keywords"],
                    "importance": skill["importance"],
                }
            )

    return requirements
