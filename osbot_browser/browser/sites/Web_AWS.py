from osbot_aws.apis.IAM import IAM

from osbot_aws.apis.Secrets import Secrets

from osbot_browser.browser.Browser_Page import Browser_Page
from osbot_browser.browser.sites.Site_Base import Site_Base


class Web_AWS(Site_Base):
    def __init__(self, headless=True):
        super().__init__(headless)
        self.server_url = 'https://console.aws.amazon.com/'

    def hello(self):
        pass


    def create_iam_user(self):
        iam = IAM()
        return iam.users(index_by='UserName')
