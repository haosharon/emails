define ["DataProvider"], (DataProvider) ->

  class ExampleProvider extends DataProvider

    init: (instances) ->
      super(instances)

    getLinks: (node, nodes, callback) ->
      data =
        node: JSON.stringify(node)
        otherNodes: JSON.stringify(nodes)
      @ajax "get_edges", data, (links) ->
        callback _.map links, (link, i) ->
          return link

    getLinkedNodes: (nodes, callback) ->
      data =
        nodes: JSON.stringify(nodes)
      @ajax "get_related_nodes", data, callback