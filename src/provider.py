import json, os

class EmailProvider(object):
  def __init__(self):
    f = open('src/data/0_json.json', 'r')
    data = json.loads(f.readline())
    self.emails = data['emails']

    nodes_set = {} # users
    self.edges = [] # emails
    for email in self.emails:
      from_field = email['From']
      to_fields = email['To']
      # add these users as nodes
      nodes_set[from_field] = True

      # add to users and edges
      for to in to_fields:
        nodes_set[to] = True
        self.edges.append((from_field, to))

      # add cc users and edges
      if 'Cc' in email:
        cc_fields = email['Cc']
        for cc in cc_fields:
          nodes_set[cc] = True
          self.edges.append((from_field, cc))

    self.nodes = nodes_set.keys()

  def get_nodes(self):
    return [n for n in self.nodes]

  def get_edges(self, node, otherNodes):
    edges = []
    for otherNode in otherNodes:
      for edge in self.edges:
        if node['text'] == edge[0] and otherNode['text'] == edge[1]:
          edges.append(edge)
        elif node['text'] == edge[1] and otherNode['text'] == edge[0]:
          edges.append(edge)

    return edges

  def get_related_nodes(self, nodes):
    related_set = {}
    for node in nodes:
      # for now, just add all users that have corresponded
      for edge in self.edges:
        if node == edge[0]:
          related_set[edge[1]] = True
        elif node == edge[1]:
          related_set[edge[0]] = True

    return related_set.keys()
