from unittest import TestCase

from osbot_utils.utils.Files import file_create_bytes
from osbot_utils.utils.Http import GET, GET_to_file

from plotly.graph_objs import *

class test_IGraph(TestCase):

    def save_png(self, fig):
        format = 'jpg'
        scale = 1
        image_bytes = fig.to_image(format=format, scale=scale)
        png_path = f"/tmp/plotly.{format}"
        file_create_bytes(path=png_path, bytes=image_bytes)

    def test_igraph_with_plotly(self):
        import igraph as ig

        url_net_science_gml = 'http://networkdata.ics.uci.edu/data/netscience/netscience.gml'
        net_science_gml = GET_to_file(url_net_science_gml, extension='.gml.txt')
        print(net_science_gml)

        G = ig.Graph.Read_GML(net_science_gml)
        labels = list(G.vs['label'])
        N = len(labels)
        E = [e.tuple for e in G.es]  # list of edges
        layt = G.layout('kk')  # kamada-kawai layout
        type(layt)



        Xn = [layt[k][0] for k in range(N)]
        Yn = [layt[k][1] for k in range(N)]
        Xe = []
        Ye = []
        for e in E:
            Xe += [layt[e[0]][0], layt[e[1]][0], None]
            Ye += [layt[e[0]][1], layt[e[1]][1], None]

        trace1 = Scatter(x=Xe,
                         y=Ye,
                         mode='lines',
                         line=dict(color='black', width=2),
                         hoverinfo='none'
                         )
        # trace2 = Scatter(x=Xn,
        #                  y=Yn,
        #                  mode='markers',
        #                  name='ntw',
        #                  marker=dict(symbol='circle-dot',
        #                              size=5,
        #                              color='#6959CD',
        #                              line=dict(color='rgb(50,50,50)', width=0.5)
        #                              ),
        #                  text=labels,
        #                  hoverinfo='text'
        #                  )

        width = 800
        height = 800

        data = [trace1]
        fig = Figure(data=data)
        #py.iplot(fig, filename='Coautorship-network-igraph')

        self.save_png(fig)