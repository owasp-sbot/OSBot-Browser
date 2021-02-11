class test_workflows_jira_API_Browser(TestCase):

    def setUp(self):
        self.api = API_Browser(headless = False)
        self.png_file = '/tmp/tmp-jira-screenshot.png'

    def test_open_jira_slack(self):
        #url = 'https://os-summit.slack.com/messages/DJ8UA0RFT/'
        url = 'https://os-summit.slack.com/messages/CK475UCJY/'
        self.api.sync__open(url)
        email = 'asd@asd.asd'
        password = "bbb"
        js_code = """$('#email').val('{0}')
                     $('#password').val('{1}')
                     $('#signin_btn').click()
                  """.format(email, password)

        self.api.sync__js_execute(js_code)

        #await self.api.screenshot(file_screenshot=self.png_file)

    @sync
    async def test_open_jira_page(self):
        from osbot_aws.apis.Secrets import Secrets
        self.api = API_Browser(headless=False)

        login_needed = False
        self.secrets_id = 'GS_BOT_GS_JIRA'

        (server, username, password) = Secrets(self.secrets_id).value_from_json_string().values()

        if login_needed:
            #Dev.pprint(server, username, password)
            await self.api.open(server + '/login.jsp')
            page = await self.api.page()
            await page.type('#login-form-username', username)
            await page.type('#login-form-password', password)
            await page.click('#login-form-submit')

        #await self.api.open(server + '/browse/GSP-95')
        #page = await self.api.page()
        #await self.api.js_execute("$('#show-more-links-link').click()")
        #from time import sleep
        #sleep(1)
        await self.api.page_size(2000,3000)

        await self.api.screenshot(file_screenshot='/tmp/tmp-jira-screenshot.png', full_page=True)
