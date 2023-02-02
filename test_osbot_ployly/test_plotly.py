from io import StringIO
from unittest import TestCase

import PIL
import numpy as np
import pandas as pd
from PIL.ImageDraw import ImageDraw, Draw
from PIL.ImageFont import ImageFont, truetype
from plotly.graph_objs import Scatter, Scatterpolar, Histogram, Pie, Scatter3d, Image
from plotly.subplots import make_subplots

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_create_bytes
from osbot_utils.utils.Http import GET_json, GET, GET_to_file, GET_bytes_to_file


class test_Plotly(TestCase):

    def save_jpg(self, fig):
        format = 'jpg'
        scale = 1
        image_bytes = fig.to_image(format=format, scale=scale)
        png_path = f"/tmp/plotly.{format}"
        file_create_bytes(path=png_path, bytes=image_bytes)
        return png_path

    def test_123(self):
        import plotly.express as px
        fig = px.bar(x=["a", "b", "c","d"], y=[1, 3, 3,5])
        #fig.write_html('first_figure.html', auto_open=True)
        self.save_jpg(fig)
        # image_bytes = fig.to_image()
        # png_path = "/tmp/plotly.png"
        # result = file_create_bytes(path=png_path, bytes=image_bytes)
        # pprint(result)

    def test_sankey(self):
        import plotly.graph_objects as go

        fig = go.Figure(data=[go.Sankey(
            node = dict(
              pad = 15,
              thickness = 20,
              line = dict(color = "black", width = 0.5),
              label = ["A1AAAA", "A2", "B1", "B2", "C1", "C2"],
              color = "blue"
            ),
            link = dict(
              source = [0, 1, 0, 2, 3, 3], # indices correspond to labels, eg A1, A2, A1, B1, ...
              target = [2, 3, 3, 4, 4, 5],
              value = [8, 4, 2, 8, 4, 2]
          ))])

        #fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
        #fig.show()
        self.save_jpg(fig)
        # image_bytes = fig.to_image()
        # png_path = "/tmp/plotly.png"
        # result = file_create_bytes(path=png_path, bytes=image_bytes)

    def test_sankey_2(self):
        import plotly.graph_objects as go
        import urllib, json

        url = 'https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json'
        #response = urllib.request.urlopen(url)
        #data = json.loads(response.read())
        data = GET_json(url)


        # override gray link colors with 'source' colors
        opacity = 0.4
        # change 'magenta' to its 'rgba' value to add opacity
        data['data'][0]['node']['color'] = ['rgba(255,0,255, 0.8)' if color == "magenta" else color for color in
                                            data['data'][0]['node']['color']]
        data['data'][0]['link']['color'] = [data['data'][0]['node']['color'][src].replace("0.8", str(opacity))
                                            for src in data['data'][0]['link']['source']]

        fig = go.Figure(data=[go.Sankey(
            valueformat=".0f",
            valuesuffix="TWh",
            # Define nodes
            node=dict(
                pad=15,
                thickness=15,
                line=dict(color="black", width=0.5),
                label=data['data'][0]['node']['label'],
                color=data['data'][0]['node']['color']
            ),
            # Add links
            link=dict(
                source=data['data'][0]['link']['source'],
                target=data['data'][0]['link']['target'],
                value=data['data'][0]['link']['value'],
                label=data['data'][0]['link']['label'],
                color=data['data'][0]['link']['color']
            ))])

        fig.update_layout(
            title_text="Energy forecast for 2050<br>Source: Department of Energy & Climate Change, Tom Counsell via <a href='https://bost.ocks.org/mike/sankey/'>Mike Bostock</a>",
            font_size=10)

        self.save_jpg(fig)


    def test_plotly_table_1(self):
        import plotly.graph_objects as go
        from plotly.colors import n_colors
        import numpy as np
        np.random.seed(1)

        colors = n_colors('rgb(255, 200, 200)', 'rgb(200, 0, 0)', 9, colortype='rgb')
        a = np.random.randint(low=0, high=9, size=10)
        b = np.random.randint(low=0, high=9, size=10)
        c = np.random.randint(low=0, high=9, size=10)

        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['<b>Column A</b>', '<b>Column B</b>', '<b>Column C</b>'],
                line_color='white', fill_color='white',
                align='center', font=dict(color='black', size=12)
            ),
            cells=dict(
                values=[a, b, c],
                line_color=[np.array(colors)[a], np.array(colors)[b], np.array(colors)[c]],
                fill_color=[np.array(colors)[a], np.array(colors)[b], np.array(colors)[c]],
                align='center', font=dict(color='white', size=11)
            ))
        ])

        self.save_jpg(fig)

    def test_table_2(self):
        import plotly.graph_objects as go

        headerColor = 'grey'
        rowEvenColor = 'lightgrey'
        rowOddColor = 'white'

        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['<b>EXPENSES</b>', '<b>Q1</b>', '<b>Q2</b>', '<b>Q3</b>', '<b>Q4</b>'],
                line_color='darkslategray',
                fill_color=headerColor,
                align=['left', 'center'],
                font=dict(color='white', size=12)
            ),
            cells=dict(
                values=[
                    ['Salaries', 'Office', 'Merchandise', 'Legal', '<b>TOTAL</b>'],
                    [1200000, 20000, 80000, 2000, 12120000],
                    [1300000, 20000, 70000, 2000, 130902000],
                    [1300000, 20000, 120000, 2000, 131222000],
                    [1400000, 20000, 90000, 2000, 14102000]],
                line_color='darkslategray',
                # 2-D list of colors for alternating rows
                fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor, rowOddColor] * 5],
                align=['left', 'center'],
                font=dict(color='darkslategray', size=11)
            ))
        ])
        self.save_jpg(fig)

    def test_gant_chart(self):
        import plotly.express as px
        import pandas as pd

        df = pd.DataFrame([
            dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28', Completion_pct=50),
            dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15', Completion_pct=25),
            dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30', Completion_pct=75)
        ])

        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Completion_pct")
        fig.update_yaxes(autorange="reversed")

        self.save_jpg(fig)


    def test_sunburst(self):
        import plotly.graph_objects as go

        import pandas as pd

        csv_data_1 = GET('https://raw.githubusercontent.com/plotly/datasets/718417069ead87650b90472464c7565dc8c2cb1c/sunburst-coffee-flavors-complete.csv')
        csv_data_2 = GET('https://raw.githubusercontent.com/plotly/datasets/718417069ead87650b90472464c7565dc8c2cb1c/coffee-flavors.csv')
        #pprint(csv_data_1)
        df1 = pd.read_csv(StringIO(csv_data_1))
        df2 = pd.read_csv(StringIO(csv_data_2))
        # return
        # df1 = pd.read_csv(
        #     'https://raw.githubusercontent.com/plotly/datasets/718417069ead87650b90472464c7565dc8c2cb1c/sunburst-coffee-flavors-complete.csv')
        # df2 = pd.read_csv(
        #     'https://raw.githubusercontent.com/plotly/datasets/718417069ead87650b90472464c7565dc8c2cb1c/coffee-flavors.csv')
        # return

        fig = go.Figure()

        fig.add_trace(go.Sunburst(
            ids=df1.ids,
            labels=df1.labels,
            parents=df1.parents,
            domain=dict(column=0)
        ))

        fig.add_trace(go.Sunburst(
            ids=df2.ids,
            labels=df2.labels,
            parents=df2.parents,
            domain=dict(column=1),
            maxdepth=2
        ))

        fig.update_layout(
            grid=dict(columns=2, rows=1),
            margin=dict(t=0, l=0, r=0, b=0)
        )
        self.save_jpg(fig)


    def test_webgl_1(self):
        import plotly.express as px

        import pandas as pd
        import numpy as np
        np.random.seed(1)

        N = 100000

        df = pd.DataFrame(dict(x=np.random.randn(N),
                               y=np.random.randn(N)))

        fig = px.scatter(df, x="x", y="y", render_mode='webgl')

        fig.update_traces(marker_line=dict(width=1, color='DarkSlateGray'))
        self.save_jpg(fig)

    def test_webgl_2(self):
        import plotly.graph_objects as go

        import numpy as np
        fig = go.Figure()

        trace_num = 10
        point_num = 5000
        for i in range(trace_num):
            fig.add_trace(
                go.Scattergl(
                    x=np.linspace(0, 1, point_num),
                    y=np.random.randn(point_num) + (i * 5)
                )
            )

        fig.update_layout(showlegend=False)
        self.save_jpg(fig)


    def test_icicle_chart(self):
        import plotly.express as px
        import pandas as pd
        vendors = ["XYZ","A", "B", "C", "D", None, "E", "F", "G", "H", None]
        sectors = ["Tech","Tech", "Tech", "Finance", "Finance", "Other", "Tech", "Tech", "Finance", "Finance", "Other"]
        regions = ["North","North", "North", "North", "North", "North","South", "South", "South", "South", "South"]
        sales = [1, 1, 3, 2, 4, 1, 2, 2, 1, 4, 1]
        df = pd.DataFrame(
            dict(vendors=vendors, sectors=sectors, regions=regions, sales=sales)
        )
        df["all"] = "all"  # in order to have a single root node
        print(df)
        fig = px.icicle(df, path=['all', 'regions', 'sectors', 'vendors'], values='sales')
        fig.update_traces(root_color='lightgrey')
        fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

        self.save_jpg(fig)

    def test_treemap_1(self):
        import plotly.express as px
        df = px.data.tips()
        fig = px.treemap(df, path=[px.Constant("all"), 'day', 'time', 'sex'], values='total_bill')
        fig.update_traces(root_color="lightgrey")
        fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
        self.save_jpg(fig)

    def test_treemap_2(self):
        import plotly.express as px
        import numpy as np
        df = px.data.gapminder()#.query("year == 1987")
        pprint(df)
        fig = px.treemap(df, path=[px.Constant("world"), 'continent', 'country'], values='pop',
                         color='lifeExp', hover_data=['iso_alpha'],
                         color_continuous_scale='RdBu',
                         color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop']))
        fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
        self.save_jpg(fig)

    def test_figure_factory_table(self):
        import plotly.figure_factory as ff

        import pandas as pd
        df = pd.read_csv(StringIO(GET('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')))

        df_sample = df[100:120]
        fig = ff.create_table(df_sample)


        self.save_jpg(fig)

    def test_table_width(self):
        import plotly.graph_objects as go
        import pandas as pd
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')

        pprint(df.columns)

        fig = go.Figure(data=[go.Table(
            columnwidth= [50,50,100,500],
            header=dict(values=list(df.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df.Rank, df.State, df.Postal, df.Population],
                       fill_color='lavender',
                       align='left'))
        ])
        #fig.update_layout(width=5000)
        self.save_jpg(fig)


    def test_table_with_graph(self):
        import plotly.graph_objs as go
        import plotly.figure_factory as ff

        # Add table data
        table_data = [['Team', 'Wins', 'Losses', 'Ties'],
                      ['Montréal<br>Canadiens', 18, 4, 0],
                      ['Dallas Stars', 18, 5, 0],
                      ['NY Rangers', 16, 5, 0],
                      ['Boston<br>Bruins', 13, 8, 0],
                      ['Chicago<br>Blackhawks', 13, 8, 0],
                      ['LA Kings', 13, 8, 0],
                      ['Ottawa<br>Senators', 12, 5, 0]]
        # Initialize a figure with ff.create_table(table_data)
        fig = ff.create_table(table_data, height_constant=60)

        # Add graph data
        teams = ['Montréal Canadiens', 'Dallas Stars', 'NY Rangers',
                 'Boston Bruins', 'Chicago Blackhawks', 'LA Kings', 'Ottawa Senators']
        GFPG = [3.54, 3.48, 3.0, 3.27, 2.83, 2.45, 3.18]
        GAPG = [2.17, 2.57, 2.0, 2.91, 2.57, 2.14, 2.77]
        # Make traces for graph
        fig.add_trace(go.Scatter(x=teams, y=GFPG,
                                 marker=dict(color='#0099ff'),
                                 name='Goals For<br>Per Game',
                                 xaxis='x2', yaxis='y2'))
        fig.add_trace(go.Scatter(x=teams, y=GAPG,
                                 marker=dict(color='#404040'),
                                 name='Goals Against<br>Per Game',
                                 xaxis='x2', yaxis='y2'))

        fig.update_layout(
            title_text='2016 Hockey Stats',
            margin={'t': 50, 'b': 100},
            xaxis={'domain': [0, .5]},
            xaxis2={'domain': [0.6, 1.]},
            yaxis2={'anchor': 'x2', 'title': 'Goals'}
        )
        self.save_jpg(fig)

    # todo: see if we really need IGRAPH
    def test_igraph(self):
        import igraph
        from igraph import Graph, EdgeSeq
        nr_vertices = 25
        v_label = list(map(str, range(nr_vertices)))
        G = Graph.Tree(nr_vertices, 2)  # 2 stands for children number
        lay = G.layout('rt')

        position = {k: lay[k] for k in range(nr_vertices)}
        Y = [lay[k][1] for k in range(nr_vertices)]
        M = max(Y)

        es = EdgeSeq(G)  # sequence of edges
        E = [e.tuple for e in G.es]  # list of edges

        L = len(position)
        Xn = [position[k][0] for k in range(L)]
        Yn = [2 * M - position[k][1] for k in range(L)]
        Xe = []
        Ye = []
        for edge in E:
            Xe += [position[edge[0]][0], position[edge[1]][0], None]
            Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]

        labels = v_label

        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Xe,
                                 y=Ye,
                                 mode='lines',
                                 line=dict(color='rgb(210,210,210)', width=1),
                                 hoverinfo='none' ,
                                 name='edges'
                                 ))
        fig.add_trace(go.Scatter(x=Xn,
                                 y=Yn,
                                 mode='markers',
                                 name='an circle',
                                 marker=dict(symbol='circle-dot',
                                             size=18,
                                             color='#6175c1',  # '#DB4551',
                                             line=dict(color='rgb(50,50,50)', width=1)
                                             ),
                                 text=labels,
                                 hoverinfo='text',
                                 opacity=0.8
                                 ))

        self.save_jpg(fig)


    def test_radar_graph(self):
        import plotly.graph_objects as go

        categories = ['processing cost', 'mechanical properties', 'chemical stability',
                      'thermal stability', 'device integration']

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=[1, 5, 2, 2, 3],
            theta=categories,
            fill='toself',
            name='Product A'
        ))
        fig.add_trace(go.Scatterpolar(
            r=[4, 3, 2.5, 1, 2],
            theta=categories,
            fill='toself',
            name='Product B'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )),
            showlegend=False
        )

        self.save_jpg(fig)

    def test_polar_graph(self):
        import plotly.express as px
        df = px.data.wind()

        # fig = px.line_polar(df, r="frequency", theta="direction", color="strength", line_close=True,
        #                     color_discrete_sequence=px.colors.sequential.Plasma_r,
        #                     template="plotly_dark", )
        #
        fig = px.scatter_polar(df, r="frequency", theta="direction",
                               color="strength", symbol="strength", size="frequency",
                               color_discrete_sequence=px.colors.sequential.Plasma_r)

        self.save_jpg(fig)

    def test_subplots(self):
        specs = [[{},{},{}],
                 [{},{},{}],
                 [{},{},{}],
                 [{},{},{}],
                 [{"type": "pie"}, {"type": "pie"},{"type": "pie"}],        # available types: xy , scene , polar, ternary, mapbox , domain  (see https://plotly.com/python/subplots/#subplots-types for more details)
                 [{"type": "scene",  "rowspan": 2}, {"colspan": 2, "rowspan": 2}, None] ,
                 [{},{},{}],
                 [{},{},{}]]
        titles = ("Plot 1", "Plot 2", "Plot 3", "Plot 4", None, "Plot 6")
        widths = [0.2, 0.3, 0.5]
        fig = make_subplots(rows=8, cols=3, specs=specs, subplot_titles=titles, column_widths=widths)

        # adding traces
        scater_1 = Scatter(x=[1, 2, 3, 4, 5], y=[5, 6, 7, 8, 9])
        scater_2 = Scatter(x=[3, 4, 5, 6, 7], y=[10, 11, 12, 9, 8])
        scater_3 = Scatter(x=[4, 5, 6, 7, 8], y=[6, 7, 8, 9, 10])

        fig.add_trace(scater_1, row=1, col=1)       # same repeated in 3 cells , same row
        fig.add_trace(scater_1, row=1, col=2)
        fig.add_trace(scater_1, row=1, col=3)

        fig.add_trace(scater_2, row=2, col=1)       # individually added
        fig.add_trace(scater_3, row=2, col=2)

        fig.add_trace(scater_1, row=2, col=3)       # all in same cell
        fig.add_trace(scater_2, row=2, col=3)
        fig.add_trace(scater_3, row=2, col=3)

        # adding histograms
        histogram_1 = Histogram(x=np.random.randn(500))
        histogram_2 = Histogram(x=np.random.randn(500))

        fig.add_trace(histogram_1, row=3 , col=1)
        fig.add_trace(histogram_2, row=3, col=2)
        fig.add_trace(histogram_2, row=3, col=3)
        fig.add_trace(histogram_1, row=4, col=1)
        fig.add_trace(histogram_2, row=4, col=1)

        fig.add_trace(scater_1   , row=4, col=2)
        fig.add_trace(histogram_1, row=4, col=2)

        # pie (needs spec with {"type": "pie"} on correct cell)
        labels = ['Oxygen', 'Hydrogen', 'Carbon_Dioxide', 'Nitrogen']
        values_1 = [4500, 2500, 1053, 500]
        values_2 = [1000, 2000, 3000, 500]
        pie_1  = Pie(labels=labels, values=values_1)
        pie_2  = Pie(labels=labels, values=values_2)

        fig.add_trace(pie_1, row=5, col=1)
        fig.add_trace(pie_2, row=5, col=2)
        fig.add_trace(pie_1, row=5, col=3)
        fig.add_trace(pie_2, row=5, col=3)

        # adding traces to the cell that has rowspan=2 and rowspan=2
        fig.add_trace(scater_1, row=6, col=2)

        # 3d trace
        trace_3d = Scatter3d(x=[2, 3, 1], y=[0, 0, 0],z=[0.5, 1, 2], mode="lines")
        fig.add_trace(trace_3d, row = 6, col = 1)


        # adding images
        fig.add_layout_image(source="https://images.plot.ly/language-icons/api-home/python-logo.png",
                             x=0.8, y=0.2, sizex=0.2, sizey=0.72, xanchor="left", yanchor="top")

        # this doesn't seem to work
        #fig.add_layout_image(source="https://images.plot.ly/language-icons/api-home/python-logo.png",
        #                    row=3, col=3)

        import plotly.express as px

        imgR    = np.random.rand(20, 40)
        img_rgb = np.array([[[255, 0, 0], [0, 255, 0], [0, 0, 255]]], dtype=np.uint8)
        image_1 = px.imshow(imgR)
        image_2 = px.imshow(img_rgb)
        fig.add_trace(image_1.data[0], row=8, col=1)
        fig.add_trace(image_2.data[0], row=8, col=2)

        local_file = GET_bytes_to_file('https://images.plot.ly/language-icons/api-home/python-logo.png')
        #img = PIL.Image.open('/tmp/jira_graph.png')
        img = PIL.Image.open(local_file)
        image_1 = Image(z=img)

        fig.add_trace(image_1                , row=8, col=3)
        fig.update_xaxes(showticklabels=False, row=8, col=3)
        fig.update_yaxes(showticklabels=False, row=8, col=3)

        # updating xaxes
        fig.update_xaxes(title_text="xaxis 3 title", showgrid=False, row=2, col=1)
        fig.update_xaxes(title_text="xaxis 4 title", type="log", row=2, col=2)



        fig.update_layout(height=800, width=1216, title_text="Subplots")
        fig.update_layout(showlegend=False)
        fig.update(layout_coloraxis_showscale=False)



        png_path = self.save_jpg(fig)

        image = PIL.Image.open(png_path)
        draw = Draw(image)
        font = truetype('Avenir.ttc', 36)

        draw.text((200, 10), "Dynamic Text (using PIL)", font=font, fill=(1, 1, 1))
        image.save(png_path)