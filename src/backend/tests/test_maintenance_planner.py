from app.services.maintenance_planner import generate_maintenance_plan


def test_plan_is_priority_ranked_1_to_n():
    plan = generate_maintenance_plan()
    ranks = [p["priority_rank"] for p in plan]
    assert ranks == list(range(1, len(plan) + 1))


def test_every_task_has_an_action_and_window():
    plan = generate_maintenance_plan()
    for task in plan:
        assert task["recommended_action"]
        assert task["recommended_window_hours"] > 0
