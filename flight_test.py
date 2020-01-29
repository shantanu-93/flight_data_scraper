#!/usr/bin/env python
#
# It's to find out max flow in a flow network
# It's similar to Ford-Fulkerson algorithm,
# but defines search order for augmenting path
# The path found must be a shortest path that has available capacity.
# http://en.wikipedia.org/wiki/Edmonds%E2%80%93Karp_algorithm
#

import decimal
import sys

def EdmondsKarp(capacity, neighbors, start, end):
  flow = 0
  length = len(capacity)
  flows = [[0 for i in range(length)] for j in range(length)]
  while True:
    max, parent = BreadthFirstSearch(capacity, neighbors, flows, start, end)
    print 'max:%s' % max
    print parent
    if max == 0:
      break
    flow = flow + max
    v = end
    while v != start:
      u = parent[v]
      flows[u][v] = flows[u][v] + max
      flows[v][u] = flows[v][u] - max
      v = u
  return (flow, flows)



def BreadthFirstSearch(capacity, neighbors, flows, start, end):
  length = len(capacity)
  parents = [-1 for i in xrange(length)] # parent table
  parents[start] = -2 # make sure source is not rediscovered
  M = [0 for i in xrange(length)] # Capacity of path to vertex i
  M[start] = decimal.Decimal('Infinity') # this is necessary!

  queue = []
  queue.append(start)
  while queue:
    u = queue.pop(0)
    for v in neighbors[u]:
      # if there is available capacity and v is is not seen before in search
      if capacity[u][v] - flows[u][v] > 0 and parents[v] == -1:
        parents[v] = u
        # it will work because at the beginning M[u] is Infinity
        M[v] = min(M[u], capacity[u][v] - flows[u][v]) # try to get smallest
        if v != end:
          queue.append(v)
        else:
          return M[end], parents
  return 0, parents


def ParseGraph(file):
  file_object = open(file, "r")
  capacity = []
  neighbors = {} # neighbors include reverse direction neighbors
  for line in file_object.readlines():
    capacity.append([int(i) for i in line.split(',')])
  for vertex in xrange(len(capacity)):
    neighbors[vertex] = []
  for vertex, flows in enumerate(capacity):
    for neighbor, flow in enumerate(flows):
      if flow > 0:
        neighbors[vertex].append(neighbor)
        neighbors[neighbor].append(vertex) # reverse path may be used
  return capacity, neighbors


def ek():
    flow, path = 0, True
    
    while path:
        # search for path with flow reserve
        path, reserve = depth_first_search(graph, source, sink)
        flow += reserve
        # increase flow along the path
        for v, u in zip(path, path[1:]):
            if graph.has_edge(v, u):
                graph[v][u]['flow'] += reserve
            else:
                graph[u][v]['flow'] -= reserve
        
        # show intermediate results
        if callable(debug):
            debug(graph, path, reserve, flow)
    

def depth_first_search(graph, source, sink):
    undirected = graph.to_undirected()
    explored = {source}
    stack = [(source, 0, undirected[source])]
    
    while stack:
        v, _, neighbours = stack[-1]
        if v == sink:
            break
        
        # search the next neighbour
        while neighbours:
            u, e = neighbours.popitem()
            if u not in explored:
                break
        else:
            stack.pop()
            continue
        
        # current flow and capacity
        in_direction = graph.has_edge(v, u)
        capacity = e['capacity']
        flow = e['flow']
        # increase or redirect flow at the edge
        if in_direction and flow < capacity:
            stack.append((u, capacity - flow, undirected[u]))
            explored.add(u)
        elif not in_direction and flow:
            stack.append((u, flow, undirected[u]))
            explored.add(u)
    # (source, sink) path and its flow reserve
    reserve = min((f for _, f, _ in stack[1:]), default=0)
    path = [v for v, _, _ in stack]
    
    return path, reserve

if __name__ == "__main__":
  file_name = sys.argv[1] # use file flow_network.txt
  capacity, neighbors = ParseGraph(file_name)
  for line in capacity:
    print line
  print neighbors
  flow, flows = EdmondsKarp(capacity, neighbors, 0, 6)
  print 'Max flow: %s' % flow
  print 'Flow matrix:'
  for line in flows:
    print line

