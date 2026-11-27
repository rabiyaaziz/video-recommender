# Decision Log

## 1. Graph storage: hashmap (dict of lists)
- **Options:** list of lists, adjacency matrix, database
- **Chose:** dict `{video_id: [related_ids]}`
- **Why:** O(1) lookup by id vs O(n) scanning a list. Trade-off: slightly more memory for much faster lookups.

## 2. Data format: JSON file
- **Why:** keeps data separate from code, human-readable, built into Python.
- **Trade-off:** fine for a small catalog. In production I'd use a database for scale,
  safe concurrent updates, access control, and querying only what's needed.
  Only `load_graph` would change.

## 3. JSON shape: list of video records
- **Why:** each video is a record with several fields (id, title, category, related);
  a list of records is the standard JSON shape. The loader converts it into the
  id → related dict the recommender needs, keeping only what's used.

## 4. Testing: pytest
- **Options:** pytest, unittest (built-in), manual print checks
- **Chose:** pytest
- **Why:** one command finds and runs every test automatically (files and
  functions named `test_*`), and shows exactly which assert failed and why.
  Plain `assert` keeps tests short and readable, vs. unittest's class boilerplate.
- **Trade-off:** one extra dependency to install, but it's the industry standard.

## 5. Ranking: count with a dict, then sort
- **Decision:** Count how many watched videos point to each related video, then sort by count (highest first).
- **Options:** A set for deduping plus separate counting, or a dict alone.
- **Why:** Dict keys are unique, so one dict both dedupes and counts. My interview version used `seen.add()` to dedupe; once I added counting, that became redundant, so I removed it. `seen` now holds only watched videos.
- **Sorting:** `.sort()` sorts in place; `sorted()` would create a copy I don't need.
- **Trade-off:** Sorting every candidate is O(m log m), even if I only need the top k. A heap could do O(m log k). I'll compare on Day 3.

## 6. Unknown video IDs
- **Decision:** Skip watched IDs that aren't in the graph (`if watch in graph`).
- **Options:** Crash with a KeyError, skip silently, or reject with an error.
- **Why:** On Day 4, `watched` comes from a URL anyone can type. One bad ID shouldn't crash recommendations for everyone.
- **Trade-off:** Skipping hides bad input. The API could return a 400 error instead (revisit on Day 4).

## 7. Separate counting from ranking
- **Decision:** Split `recommend()` into `count_related()` (builds counts) and `rank_*()` (orders them). `recommend()` just calls both.
- **Why:** Lets me swap ranking strategies without touching counting, and lets the benchmark time only the ranking step so the comparison is fair.
- **`k` parameter:** `k=None` returns all results (Python slices treat `None` as "to the end"), so existing callers didn't break. The API will pass a real k.
- **Trade-off:** Two extra function calls; negligible.