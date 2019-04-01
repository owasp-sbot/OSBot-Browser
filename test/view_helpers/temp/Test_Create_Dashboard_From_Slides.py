from unittest import TestCase

from gsuite.GSheets import GSheets
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Local_Cache import use_local_cache_if_available
from pbx_gs_python_utils.utils.aws.Lambdas import Lambdas


class Create_Dashboard_From_Slides:
    def __init__(self):
        self.file_id          = ''
        self.sheet_name       = ''
        self.gsuite_secret_id = None
        self._gsheets         = None

    def gsheets(self):
        if self._gsheets is None:
            self._gsheets = GSheets(gsuite_secret_id=self.gsuite_secret_id)
        return self._gsheets

    #@use_local_cache_if_available
    def get_r1_r2_r3_issues(self):
        params = ['search', 'label', 'R1,R2,R3']
        return Lambdas('gs.elk_to_slack').invoke({"params": params})

    def get_r1_r2_r3_model(self):
        print()
        r1_r2_r3 = self.get_r1_r2_r3_issues()
        model = {}
        for issue in r1_r2_r3:
            key    = issue.get('Key')
            labels = issue.get('Labels')
            summary  = issue.get('Summary')
            items    = summary.split('-')
            if len(items) == 1:
                print(key,summary)
            #if 'R1' in labels:
            #    model[key] = {'key' : key , 'title': title}
                #print('r1',key, title)
            #if 'R2' in labels:
                #print('r2',key, title)
            #if 'R3' in labels:
                #print('r3',key, title)
            #Dev.pprint(issue)
        #return issues
        return model
    #def add_risk_data_to_sheet(self):

    # def get_raw_sheet_data(self):
    #     return self.gsheets().all_spreadsheets()

class Test_Create_Dashboard_From_Slides(TestCase):
    def setUp(self):
        self.create_dashboard = Create_Dashboard_From_Slides()

    def test_get_r1_r2_r3_model(self):
        result = self.create_dashboard.get_r1_r2_r3_model()
        Dev.pprint(result)
    # def test_get_raw_sheet_data(self):
    #     result = self.create_dashboard.get_raw_sheet_data()
        #Dev.pprint(result)