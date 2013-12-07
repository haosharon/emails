import json

class EmailProvider(object):
  def __init__(self):
    f = open('src/data/0_json.json', 'r')
    # f = open('src/data/my_json.json', 'r')
    data = json.loads(f.readline())
    self.emails = data['emails']
    self.nodes = set() # users
    self.edges = {}    # emails - self.edges[sender][recipient]=count
    self.max_emails = 0.0
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
              self.edges[from_field].setdefault(recipient, 0)
              self.edges[from_field][recipient] += 1

              self.edges.setdefault(recipient, {})
              self.edges[recipient].setdefault(from_field, 0)

              self.max_emails = max(self.edges[from_field][recipient] + self.edges[recipient][from_field], self.max_emails)


  def get_nodes(self):
    return [n for n in self.nodes]

  def get_edges(self, node, otherNodes):
    # return an dictionary of node strengths and directions
    links = []
    for otherNode in otherNodes:
      val = 0
      a, b = node["text"], otherNode["text"]
      direction = 0
      val = 0
      if a in self.edges and b in self.edges[a]:
        if self.edges[a][b] > 0:
          direction += 1
          val += self.edges[a][b]
      if b in self.edges and a in self.edges[b]:
        if self.edges[b][a] > 0:
          direction += 2
          val += self.edges[b][a]
      dic = {}
      strength = min(1, 100.0 * val / self.max_emails)
      dic['strength'] = strength
      if direction == 0:
        dic['direction'] = 'null'
      elif direction == 1:
        dic['direction'] = 'forward'
      elif direction == 2:
        dic['direction'] = 'backward'
      else:
        dic['direction'] = 'bidirectional'
      # if b in self.edges[a] or a in self.edges[b]:
      #   val = self.edges[a][b] / self.normalized
      # strengths.append(val)
      links.append(dic)
    return links

  def get_related_nodes(self, nodes):
    related = set()
    for node in nodes:
      # for now, just add all users that have corresponded
      text = node['text']
      if text in self.edges:
        for recipient in self.edges[node["text"]]:
          related.add(recipient)
      for key in self.edges.keys():
        val = self.edges[key]
        if text in val:
          related.add(key)
    return list(related)
