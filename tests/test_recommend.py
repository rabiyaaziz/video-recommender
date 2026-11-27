from recommender.loader import load_graph
from recommender.recommend import recommend
from recommender.recommend import rank_sort, rank_heap, count_related
from recommender.recommend import recommend, rank_sort, rank_heap, rank_bucket, count_related


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

def test_top_k():
    result = recommend(["v1", "v4"], graph, k=1)
    assert result == ["v5"]

def test_heap_matches_sort():
    counts = count_related(["v1", "v4"], graph)
    assert rank_heap(counts, 1) == rank_sort(counts, 1)

def test_bucket_matches_sort():
    counts = count_related(["v1", "v4"], graph)
    assert rank_bucket(counts, 1) == rank_sort(counts, 1)

def test_all_strategies_break_ties_the_same():
    counts = {"v6": 1, "v2": 1, "v5": 2}
    expected = ["v5", "v2", "v6"]
    assert rank_sort(counts, None) == expected
    assert rank_heap(counts, None) == expected
    assert rank_bucket(counts, None) == expected