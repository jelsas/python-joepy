from itertools import chain

class Graph(object):
  '''A graph is just a list of edges + a weight.
  Each edge is stored as a 3-tuple, (from_vertex, to_vertex, weight).'''
  def __init__(self):
    self.edges = []

  def add_edge(self, from_vertex, to_vertex, weight=1):
    if weight < 0:
      raise ValueError('We don\'t deal with negative weights so well here')
    self.edges.append( (from_vertex, to_vertex, weight) )

  def reverse(self):
    '''Reverses the direction of all the edges, modifying the graph in place'''
    self.edges = [(t, f, w) for (f, t, w) in self.edges]

  def vertices(self):
    return set(t for (f, t, w) in self.edges) | \
            set(f for (f, t, w) in self.edges)

  def edges_from(self, from_vertex):
    return [ (f, t, w) for (f, t, w) in self.edges if f == from_vertex ]

  def edges_to(self, to_vertex):
    return [ (f, t, w) for (f, t, w) in self.edges if t == to_vertex ]

  def terminals(self):
    '''returns the nodes that have no out-links.'''
    non_terminals = set( f for (f, t, w) in self.edges )
    return set( t for (f, t, w) in self.edges if t not in non_terminals )

  def empty(self):
    return len(self.edges) == 0

  def is_acyclic(self, min_edge_weight = 0):
    '''Tests whether there are any cycles in this graph.  Optionally can ignore
    edges with a weight under the given threshold.'''
    g = Graph()
    g.edges = [(f, t, w) for (f, t, w) in self.edges if w >= min_edge_weight]
    while True:
      # if we've removed all the edges, we're done
      if g.empty(): return True
      terminals = g.terminals()
      # if there's no terminals (and g is non-empty) then there's a cycle
      if len(terminals) == 0: return False
      # strip off all the edges that point to terminal nodes
      g.edges = [(f, t, w) for (f, t, w) in g.edges if t not in terminals]

  def shortest_path(self, source):
    '''Djikstra's algorithm, returns the length of the shortest path to all
    accessible vertices from the provided source.  O(|V|**2)'''
    INF = 1e1000

    def min_entry(dists, Q):
      '''finds the key with the minimum value in dict d'''
      min_k, min_v = None, None
      for k in Q:
        v = dists[k]
        if min_k is None or v < min_v:
          min_k, min_v = k, v
      return min_k, min_v

    vertices = self.vertices()
    if source not in vertices:
      raise ValueError('source is not in this graph')

    dists = dict( (x, INF) for x in vertices )
    previous = dict( (x, None) for x in vertices )
    dists[source] = 0

    while len(vertices) > 0:
      u, u_dist = min_entry(dists, vertices)
      if u_dist == INF: break
      vertices.discard(u)
      for (_, v, w) in self.edges_from(u):
        alt = u_dist + w
        if alt < dists[v]:
          dists[v] = alt
          previous[v] = u

    # remove the inaccessible nodes
    dists = dict( (k, v) for (k, v) in dists.iteritems() if v < INF )
    return dists

  def all_path_lengths(self):
    '''The Floyd-Warshall algorithm to find the distance of all minimum-
    length paths between any two vetices.  Returns a dictionary such that
    d[(i, j)] is the shortest path between nodes i and j.  If no such path
    exists, this key won't be present in the dictionary.  O(|V|**3)'''
    d = dict()
    for (f, t, w) in self.edges:
      d[(f, t)] = w
    vertices = self.vertices()
    for k in vertices:
      for i in vertices:
        if i == k: continue
        try:
          d_i_k = d[(i,k)]
        except KeyError:
          # if i doesn't reach k, then no need to proceed
          continue
        for j in vertices:
          if i == j or j == k: continue
          d_k_j = d.get((k, j))
          d_i_j = d.get((i, j))
          # if k->j, we update d[(i,j)], otherwise leave untouched
          if d_k_j is not None:
            d[(i, j)] = min(d_i_j, d_i_k + d_k_j) if d_i_j else d_i_k + d_k_j
    return d

  def reachable_from(self, source):
    return set(self.shortest_path(source).keys())

  def to_graphvis(self, node_formatter = str):
    '''Returns a string representation of this graph in a format readable by
    GraphVis: http://www.graphviz.org/doc/info/lang.html .  Optionally, a
    node_formatter can be specified which takes the node type and produces a
    string.  Defaults to the built-in str function.'''
    def graphvis_edge( edge ):
      (f, t, w) = edge
      if w == 0:
        modifier = '[style=dotted]'
      elif w > 1:
        modifier = '[weight=%d]' % w
      else:
        modifier = ''
      return '%s->%s%s' % (node_formatter(f), node_formatter(t), modifier)
    return 'digraph{%s}' % ';'.join( graphvis_edge(e) for e in self.edges )
