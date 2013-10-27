import json, os

class EmailProvider(object):
  def __init__(self):
    f = open('src/data/0_json.json', 'r')
    data = json.loads(f.readline())
    self.emails = data['emails']

    nodes_set = {} # users
    self.links = [] # emails
    for email in self.emails:
      from_field = email['From']
      to_field = email['To']
      # add these users as nodes
      nodes_set[to_field] = True
      nodes_set[from_field] = True
      self.links.append((from_field, to_field))
      if 'Cc' in email:
        cc_field = email['Cc']
        nodes_set[cc_field] = True
        self.links.append((from_field, cc_field))

    self.nodes = nodes_set.keys()

  def get_nodes(self):
    return [n for n in self.nodes]

  def get_edges(self, node, otherNodes):
    edges = []
    for otherNode in otherNodes:
      for edge in self.edges:
        if node == edge[0] and otherNode == edge[1]:
          edges.append(edge)
        elif node == edge[1] and otherNode == edge[0]:
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
