from validators import validate_competition_date


valid_competition_data = {
    "date": "2025-09-22T10:00:00.000Z",
}

invalid_competition_data = {
    "date": "2024-09-22T10:00:00.000Z",
}

def test_validate_competition_date():
    assert validate_competition_date(valid_competition_data) is None
    assert validate_competition_date(
        invalid_competition_data
    ) == "You cannot book past competitions"