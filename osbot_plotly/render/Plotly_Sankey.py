from osbot_jira.data.COLORS_BY_PROJECT import COLORS_BY_PROJECT
from osbot_plotly.render.Plotly_Base import Plotly_Base
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import word_wrap


class Plotly_Sankey(Plotly_Base):

    def __init__(self):
        super().__init__()
        self.text_font_size = 4
        self.text_max_width = 40
        #self.text

    def mvp(self):
        import plotly.graph_objects as go

        labels = ["start", "A1", "B1", "B2", "C1", "C2QQ","AAAAA"]
        source = [0   , 0  , 0  , 2   , 3 ] # , 3 , 2]
        target = [6   , 3  , 1  , 3   , 4 ] # , 5 , 7]
        value  = [1   , 1  , 1  , 1   , 1 ] # , 1 , 1]
        color  = "blue"

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=color
            ),
            link=dict(
                source=source  ,
                target=target  ,
                value=value
            ))])

        # fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
        # fig.show()
        self.set_figure(fig)

        fig.update_traces(orientation="h")
        fig.update_traces(arrangement="fixed") # snap , perpendicular , freeform

        self.save_as_jpg()

    def create_from_nx_graph(self, nx_graph):
        import plotly.graph_objects as go
        # Create a dictionary that maps each node label to its index
        nx_nodes = nx_graph.nodes()
        #nodes = list()
        nodes_texts = []
        nodes_ids   = []
        colors      = []

        for node_id, node_data in nx_nodes.items():
            key       = node_data.get('key')
            text      = node_data.get('text') or node_id
            project   = node_data.get('project')
            node_text = f"{key} - {text}"[0:self.text_max_width]
            #node_value = {"text": node_text, "font": {"size": 20}}
            nodes_texts.append(node_text)
            nodes_ids .append(node_id)
            color = COLORS_BY_PROJECT.get(project)
            if color is None:
                print(f"[Plotly_Sankey] no color for project {project}")
            colors.append(color or "aliceblue")

        node_indices = {nodes_ids[i]: i for i in range(len(nodes_ids))}

        # Use the dictionary to convert the node labels in the sources and targets lists to indices
        edges = nx_graph.edges()
        sources = [node_indices[edge[0]] for edge in edges]
        targets = [node_indices[edge[1]] for edge in edges]
        value   = [1] * len(nodes_ids)
        #pprint(value)

        #pprint(sources)
        #pprint(targets)

        # Create a Sankey diagram using plotly
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad         = 25,
                thickness   = 20,
                line        = dict(color="black", width=0.5),
                label       = nodes_texts,
                #textfont    = dict(size=200) ,
                color       = colors ,
            ),
            link=dict(
                source =sources,
                target =targets,
                value =value ,
            ))])
        fig.update_layout(font=dict(size=self.text_font_size))

        #fig.update_traces(arrangement="snap")
        self.set_figure(fig)
        return self
