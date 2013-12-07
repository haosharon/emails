requirejs.config
  baseUrl: "/scripts/celestrium/core/"

  paths:
    local: "../../"

require ["Celestrium"], (Celestrium) ->

  plugins =

    Layout:
      el: document.querySelector("body")

    KeyListener:
      document.querySelector("body")

    GraphModel:
      nodeHash: (node) -> node.text
      linkHash: (link) -> link.source.text + link.target.text

    GraphView: {}
    Sliders: {}
    ForceSliders:
      pluginOrder: 1
    NodeSearch:
      pluginOrder: 0
      prefetch: "get_nodes"

    Stats:
      pluginOrder: 2
    NodeSelection: {}
    LinkDistribution:
      pluginOrder: 3
    SelectionLayer: {}
    "local/ExampleDataProvider": {}

  Celestrium.init plugins, (instances) ->
    instances["GraphView"].getLinkFilter().set("threshold", 0)