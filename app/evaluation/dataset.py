from app.evaluation.models import EvaluationQuery


EVALUATION_DATASET = [

    EvaluationQuery(
        query="How does authentication work?",
        repository_id=1,
        relevant_sources=[
            "app/services/auth_service.py",
            "app/api/auth.py",
        ],
    ),

    EvaluationQuery(
        query="How is the database connection configured?",
        repository_id=1,
        relevant_sources=[
            "app/core/config.py",
            "app/db/database.py",
        ],
    ),

    EvaluationQuery(
        query="How is the application started?",
        repository_id=1,
        relevant_sources=[
            "app/main.py",
        ],
    ),
]