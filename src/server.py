import os, sys, cherrypy, provider
import simplejson as json

'''USAGE: python src/server.py <knowledgebase-uri> <num-axes> <concepts|assertions> <port>'''

portStr = sys.argv[1]

class Server(object):

  _cp_config = {'tools.staticdir.on' : True,
                'tools.staticdir.dir' : os.path.abspath(os.path.join(os.getcwd(), "src/www")),
                'tools.staticdir.index' : 'index.html',
                }

  def __init__(self):
    self.provider = provider.EmailProvider()

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def get_nodes(self):
    return self.provider.get_nodes()

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def get_edges(self, node, otherNodes):
    return self.provider.get_edges(json.loads(node), json.loads(otherNodes))

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def get_related_nodes(self, nodes):
    related_nodes = self.provider.get_related_nodes(json.loads(nodes))

    return [{'text': node} for node in related_nodes]

cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': int(portStr),
                       })

cherrypy.quickstart(Server())
