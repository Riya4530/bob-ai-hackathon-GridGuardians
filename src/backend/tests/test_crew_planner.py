from app.services.crew_planner import generate_crew_plan


def test_no_crew_double_booked():
    plan = generate_crew_plan()
    crew_ids = [p["crew_id"] for p in plan]
    assert len(crew_ids) == len(set(crew_ids))


def test_every_assignment_targets_a_real_asset():
    plan = generate_crew_plan()
    for assignment in plan:
        assert assignment["target_asset_id"]
        assert assignment["pre_position_before_hours"] > 0
