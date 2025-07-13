from server import load_data, save_json, save_clubs_and_competitions


def test_load_data():
    """Test that the load_data function returns the correct data"""
    data = load_data("clubs.json", "clubs")
    assert data is not None
    assert len(data) == 3
    assert "name" in data[0].keys()
    assert "email" in data[0].keys()
    assert "points" in data[0].keys()

def test_save_json():
    """Test that the save_json function saves the correct data"""
    data = load_data("clubs.json", "clubs")
    save_json("clubs.json", data, "clubs")
    assert load_data("clubs.json", "clubs") == data

