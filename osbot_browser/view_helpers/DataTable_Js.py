from osbot_browser.browser.API_Browser import API_Browser
from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from osbot_browser.browser.Render_Page import Render_Page
from pbx_gs_python_utils.utils.Files import Files


class DataTable_Js:

    def __init__(self):
        self.web_page     = '/datatables/simple.html'
        self.web_root     = Files.path_combine(Files.parent_folder(__file__),'../web_root')
        self.api_browser  = API_Browser().sync__setup_browser()
        self.render_page  = Render_Page(api_browser=self.api_browser, web_root=self.web_root)
        self.table_width  = '100%'
        self.columns_defs = None
        self.table_title  = None

    # helper methods (to move to base class)
    def browser(self):
        return self.api_browser

    def show_chrome(self):
        self.render_page.api_browser.headless   = False
        self.render_page.api_browser.auto_close = False
        return self

    def load_page(self,reload=False):
        if reload or self.web_page not in self.browser().sync__url():
            self.render_page.open_file_in_browser(self.web_page)
        return self

    def js_execute(self, name,params=None):
        return self.browser().sync_js_invoke_function(name,params)

    def js_eval(self, js_code):
        return self.browser().sync__js_execute(js_code)

    def send_screenshot_to_slack(self, team_id, channel):
        png_file = self.create_dashboard_screenshot()
        return Browser_Lamdba_Helper().send_png_file_to_slack(team_id, channel, 'risk dashboard', png_file)

    def create_dashboard_screenshot(self):
        #clip = {'x': 1, 'y': 1, 'width': 945, 'height': 465}
        clip = None
        return self.browser().sync__screenshot(clip=clip)

    # main datatable methods

    def create_table(self, headers, rows):
        self.load_page(True)

        columns = []
        for header in headers:
            columns.append({'title': header}),

        # headers_html = ""
        # for header in headers:
        #     headers_html += "<th>{0}</th>".format(header)
        #
        # headers_html = "<tr>{0}</tr>".format(headers_html)
        #
        # rows_html = ""
        # for row in rows:
        #     row_html = ""
        #     for cell in row:
        #         row_html += "<td>{0}</td>".format(cell)
        #     row_html = "<tr>{0}</tr>\n".format(row_html)
        #     Dev.print(rows_html)
        #     rows_html += row_html
        #
        # #rows_html    = "<tr><td>an row</td></tr>"
        #
        # table_html   = """  <table id='{table_id}' class='display'>
        #                         <thead>
        #                             {headers}
        #                         </thead>
        #                         <tbody>
        #                             {rows}
        #                         </tbody>
        #                     </table>
        #                     """.format(table_id=table_id,headers=headers_html, rows = rows_html)

        #self.js_execute("$('#dynamic_data_table').html",table_html)

        options = {
            'columns'    : columns,
            "columnDefs" : self.columns_defs   ,
            'data'       : rows   ,
            "paging"     : False  ,
            "ordering"   : False  ,
            "info"       : False  ,
            "searching"  : False
        }
        table_html = '<table id="data_table" class="display" width="{0}"></table>'.format(self.table_width)
        self.js_execute("$('#dynamic_data_table').html",table_html)     # create table html element
        self.js_eval("$.fn.dataTable.ext.errMode = 'none';")         # disable table errors

        self.js_execute("$('#data_table').DataTable",options)           # create table
        if self.table_title:
            self.js_execute("$('#table_title').html", self.table_title)

        return self

        # js_code = """$('#data_table').DataTable({
        #             "paging"     : false,
        #             "ordering"   : false,
        #             "info"       : false,
        #             "searching"  : false
        #         });"""
        # self.js_eval(js_code)
        # return table_html