from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_browser.browser.sites.Web_AWS import Web_AWS


class Test_Web_AWS(Test_Helper):
    def setUp(self):
        super().setUp()
        self.headless = False
        self.aws = Web_AWS(self.headless).setup()


    def test_setup(self):
        self.result = self.aws.secrets_id

        #Secrets
        #self.result = Secrets(self.aws.secrets_id).value_from_json_string()

    def test_open(self):
        self.result = self.aws.open()

    def test_login(self):
        #self.aws.logout()
        self.result = self.aws.login()
        #self.png_data = self.aws.screenshot()


    def test_page_billing(self):
        self.aws.page_billing()

    def test_create_iam_user(self):
        self.result = self.aws.create_iam_user()


