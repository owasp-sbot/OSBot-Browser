from osbot_browser.view_helpers.Base_View_Helper import Base_View_Helpers


class Xml_Report(Base_View_Helpers):
    def __init__(self, headless=True, layout=None):
        if layout:
            self.web_page = '/sow/{0}.html'.format(layout)
        else:
            self.web_page = '/gw/xml-report-exec-summary.html'

        super().__init__(web_page=self.web_page, headless=headless)

    def html_table(self, div_id, title):
        return  f"""<table class="table">
                        <thead>
                            <tr>
                                <th scope="col" style="text-align: center">{title}</th>
                            </tr>
                        </thead>
                    <tbody id="{div_id}"/>
                </table>"""

    def add_to_body(self,html):
        self.invoke_js(f"$('body').append", html)

    def add_rows(self, div_id, items):
        for item in items:
            self.exec_js(f"$('#{div_id}').append('<tr><td>{item}</td></tr>')")

    def add_table(self, div_id, title, items):
        self.add_to_body(self.html_table(div_id, title))
        self.add_rows   (div_id, items)

    def set_field(self, field_id, value):
        self.invoke_js(f"$('#{field_id}').html", value)

    def add_threat(self, item):
        html_threat = f'<span class="badge badge-danger">{item}</span>'
        self.invoke_js(f"$('#threats').append", html_threat)

    def add_threats(self, items):
        if "Macros present in Type" in items:
            self.add_threat('Macros Detected and Removed')
        if "Javascript content present." in items:
            self.add_threat('Javascript Detected and Removed')

    def gw_exec_summary(self, file_name, json_data):
        self.load_page(True)
        self.set_field('file_name', file_name)
        self.set_field('file_size', json_data.get('file_size'))
        self.set_field('file_type', json_data.get('file_type'))
        self.add_table("sanitised_content", "Active content that has been Sanitised (removed)", json_data.get('sanitisation_items'))
        self.add_table("remedy_items", "Objects & Structures that have been repaired", json_data.get('remedy_items'))

        self.add_threats(json_data.get('sanitisation_items'))
        #self.browser().sync__browser_width(600,10)

        return self.browser().sync__screenshot_base64()

