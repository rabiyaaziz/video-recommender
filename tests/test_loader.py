from recommender.loader import load_graph

def test_load_graph():
    graph = load_graph("data/videos.json")
    assert graph["v1"] == ["v2", "v4", "v5"]
    assert graph["v3"] == []