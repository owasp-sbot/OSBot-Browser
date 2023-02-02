import plotly.graph_objects as go
from osbot_plotly.render.Plotly_Base import Plotly_Base


class Plotly_Table(Plotly_Base):

    def __init__(self, width=None, height=None, title=None, columns_width=None, font_size=11):
        super().__init__()
        self.width         = width         or 800
        self.height        = height        or 600
        self.title         = title         or "Table from DataFrame"
        self.columns_width = columns_width or [100,300]
        self.font_size     = font_size     or 15

    def create_table_from_df(self, df):
        headers       = list(df.columns)
        values        = [df[col] for col in df.columns]
        columns_width = self.columns_width
        table = go.Table(
            columnwidth=columns_width,
            header=dict(values=headers, align='left'),
            cells=dict(values=values  , align='left', font=dict(size=self.font_size, color='black')))

        fig = go.Figure(data=table)
        fig.update_layout(width=self.width,
                          height    = self.height,
                          title     = dict(text = self.title,
                                           y    = 0.99      ,
                                           x    = 0.01      ,
                                           font = dict(size=20)),
                          margin    = dict(l=5, r=5, t=40, b=5))
        self.set_figure(fig)
        return self

    def create_jpg_from_df(self, df):
        self.create_table_from_df(df)
        return self.save_as_jpg()
