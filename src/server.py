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
    # matrix = knowledgebase.getMatrix(knowledgebaseURI)
    # self.graph = graph.createGraph(matrix.svd(k=numAxes), graphType)
    # if graphType == 'assertions':
    #   Server._cp_config['tools.staticdir.index'] = 'index-assertions.html'
    self.provider = provider.EmailProvider()

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def get_nodes(self):
    # return self.graph.get_nodes()
    print 'getting nodes!!!'
    print 'nodes'
    nodes = self.provider.get_nodes()
    print nodes
    return nodes

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def get_edges(self, node, otherNodes):
    # return self.graph.get_edges(json.loads(node), json.loads(otherNodes))
    print 'getting edges!!!!'
    edges = self.provider.get_edges(json.loads(node), json.loads(otherNodes))
    print 'edges'
    print edges
    return edges
    #return self.provider.get_edges(json.loads(node), json.loads(otherNodes))

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def get_related_nodes(self, nodes):
    print 'nodes!!!'
    print nodes
    related_nodes = self.provider.get_related_nodes(json.loads(nodes))
    # return self.graph.get_related_nodes(json.loads(nodes), float(minStrength))
    print related_nodes
    return related_nodes

cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': int(portStr),
                       })

cherrypy.quickstart(Server())
