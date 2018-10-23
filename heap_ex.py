import heapq

a = [(1, 'A', 4), (1, 'A', 3), (1, 'A', 2)]

li = []

heapq.heapify(li)

for elem in a:
    heapq.heappush(li, elem)


while len(li) > 0:
    print heapq.heappop(li)