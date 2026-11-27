def recommend(watched, graph, k=None):
    """Return related videos for a watch history,
    excluding ones already watched, most-recommended first."""

    counts=count_related(watched,graph)
    return rank_sort(counts,k)

    

def count_related(watched, graph):
    seen=set()
    priority_map={}
    
    for watch in watched:
        seen.add(watch)
    
    for watch in watched:
        if watch in graph:
            related=graph[watch]
            for reco in related:
                if reco not in seen:
                    if reco not in priority_map:
                        priority_map[reco]=1
                    else:
                        priority_map[reco]+=1
    return priority_map

def rank_sort(counts,k):
    priority_list=[]
    for video,count in counts.items():
        priority_list.append((count,video))
    priority_list.sort(reverse=True) 

    results=[]
    for count,name in priority_list:
        results.append(name)

    return results[:k]


        