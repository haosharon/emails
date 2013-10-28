import json, os

class EmailProvider(object):
  def __init__(self):
    f = open('src/data/0_json.json', 'r')
    data = json.loads(f.readline())
    self.emails = data['emails']

    self.nodes = set() # users
    self.edges = set() # emails
    for email in self.emails:
      from_field = email['From'].strip()
      if len(from_field) > 0:
        to_fields = email['To']
        # add these users as nodes
        self.nodes.add(from_field)

        # add to users and edges
        for to in to_fields:
          to = to.strip()
          if len(to) > 0:
            self.nodes.add(to)
            self.edges.add((from_field, to))

        # add cc users and edges
        if 'Cc' in email:
          cc_fields = email['Cc']
          for cc in cc_fields:
            cc = cc.strip()
            if len(cc) > 0:
              self.nodes.add(cc)
              self.edges.add((from_field, cc))

  def get_nodes(self):
    return [n for n in self.nodes]

  def get_edges(self, node, otherNodes):
    # return an array of node strengths
    strengths = []
    for otherNode in otherNodes:
      val = 0
      for edge in self.edges:
        if node["text"] == edge[0] and otherNode['text'] == edge[1]:
          val = 0.9
          break
        elif node["text"] == edge[1] and otherNode['text'] == edge[0]:
          val = 0.9
          break
      strengths.append(val)

    return strengths

  def get_related_nodes(self, nodes):
    related_set = {}
    for node in nodes:
      # for now, just add all users that have corresponded
      for edge in self.edges:
        if node['text'] == edge[0]:
          related_set[edge[1]] = True
        elif node['text'] == edge[1]:
          related_set[edge[0]] = True

    return related_set.keys()
