import json

class EmailProvider(object):
  def __init__(self):
    f = open('src/data/0_json.json', 'r')
    data = json.loads(f.readline())
    self.emails = data['emails']
    self.nodes = set() # users
    self.edges = {}    # emails - self.edges[sender][recipient]=True if exists
    for email in self.emails:
      from_field = email['From'].strip()
      if len(from_field) > 0:
        self.nodes.add(from_field)
        for recipients in email.get('Cc', []), email.get('To', []):
          for recipient in recipients:
            recipient = recipient.strip()
            if len(recipient) > 0:
              self.nodes.add(recipient)
              # could put arbitary data here instead of just True
              # could only put one direction to make directed graph
              self.edges.setdefault(from_field, {})
              self.edges[from_field][recipient] = True
              self.edges.setdefault(recipient, {})
              self.edges[recipient][from_field] = True

  def get_nodes(self):
    return [n for n in self.nodes]

  def get_edges(self, node, otherNodes):
    # return an array of node strengths
    strengths = []
    for otherNode in otherNodes:
      val = 0
      a, b = node["text"], otherNode["text"]
      if b in self.edges[a] or a in self.edges[b]:
        val = 0.9
      strengths.append(val)
    return strengths

  def get_related_nodes(self, nodes):
    related = set()
    for node in nodes:
      # for now, just add all users that have corresponded
      for recipient in self.edges[node["text"]]:
        related.add(recipient)
    return list(related)
