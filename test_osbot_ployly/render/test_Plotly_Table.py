from unittest import TestCase

from osbot_plotly.render.Plotly_Table import Plotly_Table


class test_Plotly_Table(TestCase):

    def setUp(self) -> None:
        self.plotly_table = Plotly_Table()


    def test_create_jpg_from_df(self):
        import pandas as pd
        from io import StringIO
        from osbot_utils.utils.Http import GET

        df = pd.read_csv(
            StringIO(GET('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')))

        df_sample = df[100:110]
        self.plotly_table.create_jpg_from_df(df_sample)
