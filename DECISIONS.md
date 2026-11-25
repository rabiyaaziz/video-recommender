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