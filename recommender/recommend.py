import heapq


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


def rank_heap(counts, k):
    heap=[]

    if k==0:
        return []
    if k is None:
        k=len(counts)        

    for video,count in counts.items():
        if len(heap)<k:
            heapq.heappush(heap,(count,video))
        else:
            if heap[0][0]<count:
                heapq.heappop(heap)
                heapq.heappush(heap,(count,video))

    results=[0]*len(heap)
    index=len(heap)-1
    while heap:
        count,video=heapq.heappop(heap)
        results[index]=video
        index-=1

    return results


def rank_bucket(counts, k):
    if not counts or k==0:
        return []

    if k is None or k>len(counts):
        k=len(counts)

    max_count=max(counts.values())

    buckets=[0]*(max_count+1)

    for video,count in counts.items():
        if buckets[count]==0:
            buckets[count]=[video]
        else:
            buckets[count].append(video)

    results=[]
    
    for index in range(len(buckets)-1,-1,-1):
        if buckets[index]!=0:
            for video in buckets[index]:
                results.append(video)
                if len(results)==k:
                    return results

    return results



        