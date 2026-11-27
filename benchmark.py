import random
import time

from recommender.recommend import count_related, rank_sort, rank_heap, rank_bucket

random.seed(42)          # same fake data every run (deterministic!)

NUM_VIDEOS = 10000
RELATED_PER_VIDEO = 50
NUM_WATCHED = 200
RUNS = 50                # repeat each test, then average

# 1. Build a fake catalog: v0 ... v9999, each with 50 random related videos
ids = []
for i in range(NUM_VIDEOS):
    ids.append("v" + str(i))

graph = {}
for video in ids:
    graph[video] = random.sample(ids, RELATED_PER_VIDEO)

# 2. Fake watch history, counted ONCE (not timed)
watched = random.sample(ids, NUM_WATCHED)
counts = count_related(watched, graph)
print("candidates (m):", len(counts))


# 3. Time only the ranking step
def time_it(rank, k):
    start = time.perf_counter()
    for run in range(RUNS):
        rank(counts, k)
    end = time.perf_counter()
    return (end - start) / RUNS * 1000      # average ms per run


for k in [10, None]:
    print("\nk =", k)
    print("sort:  ", round(time_it(rank_sort, k), 3), "ms")
    print("heap:  ", round(time_it(rank_heap, k), 3), "ms")
    print("bucket:", round(time_it(rank_bucket, k), 3), "ms")