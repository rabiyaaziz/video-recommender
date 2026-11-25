import json

def load_graph(path):
    """Return {video_id: [related_ids]} from a JSON file."""
    with open(path) as f:
        videos = json.load(f)
    graph = {}
    for video in videos:
        graph[video["id"]] = video["related"]
    return graph