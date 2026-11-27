from recommender.loader import load_graph
from recommender.recommend import recommend

graph = load_graph("data/videos.json")

def test_most_common_first():
    result = recommend(["v1", "v4"], graph)
    assert result[0] == "v5"
    assert "v1" not in result
    assert "v4" not in result

def test_empty_history():
    result = recommend([], graph)
    assert result == []

def test_no_related_videos():
    result = recommend(["v3"], graph)
    assert result == []

def test_unknown_id():
    result = recommend(["v10"], graph)
    assert result == []