from pbx_gs_python_utils.utils.Dev import Dev


class Edge_Format:

    @staticmethod
    def no_labels(edges):
        for edge in edges:
            edge['label'] = ''

        return Edge_Format

    @staticmethod
    def removed_non_risk_edge_sinks(edges,nodes):       # doesn't handle well linked vulns
        sources = []
        sinks   = []
        #Dev.pprint(edges)
        for edge in edges:
            sources.append(edge.get('from'))
            sinks.append(edge.get('to'))
        sources = list(set(sources))
        sinks   = list(set(sinks))

        sinks_to_remove = []
        for sink in sinks:
            if sink not in sources:
                if sink.split('-')[0] != 'RISK':
                    sinks_to_remove.append(sink)

        #Dev.pprint(sinks_to_remove)
        for node in list(nodes):
            if node.get('id') in sinks_to_remove:
                nodes.remove(node)

        return Edge_Format

    # @staticmethod
    # def calculate_links_scores(edges, nodes):
    #
    #     from pbx_gs_python_utils.utils.aws.Lambdas import Lambdas
    #
    #     graph_paths = Lambdas('gs.graph_paths')
    #
    #     payload = { "graph_name" : 'graph_DGK', 'destination_node' : 'GSSP-6'}
    #     result = graph_paths.invoke(payload)
    #     Dev.pprint(result)
    #     return
    #
    #     for edge in edges:
    #         from_id = edge.get('from')
    #         to_id   = edge.get('to')
    #         G.add_edge(to_id, from_id)
    #
    #     # Dev.pprint(edges)
    #     # scores = {}
    #     # for edge in edges:
    #     #     from_id = edge.get('from')
    #     #     to_id   = edge.get('to')
    #     #     if scores.get(from_id) is None: scores[from_id] = { 'score' : 0}
    #     #     scores.get(from_id)['score'] += 1
    #     all_paths = {}
    #     for node in list(nodes):
    #         node_id = node.get('id')
    #         if 'RISK-' in node_id:
    #             #all_paths[node_id]= \
    #             Dev.pprint(list(nx.all_simple_paths(G,node_id,'GSSP-6')))
    #
    #     #Dev.pprint(all_paths)



