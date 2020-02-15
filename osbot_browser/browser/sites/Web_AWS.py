from osbot_aws.apis.IAM import IAM

from osbot_aws.apis.Secrets import Secrets
from osbot_aws.helpers.IAM_User import IAM_User

from osbot_browser.browser.Browser_Page import Browser_Page
from osbot_browser.browser.sites.Site_Base import Site_Base


class Web_AWS(Site_Base):
    def __init__(self, headless=True):
        super().__init__(headless)
        self.server_url = 'https://console.aws.amazon.com/'

    def login(self):

        (account_id,username,password) = Secrets(self.secrets_id).value_from_json_string().values()
        login_url = f'https://{account_id}.signin.aws.amazon.com/console'

        self.page.open(login_url)
        self.page.wait_for_element__id('username')
        js_code = f"""
                        $('#username').val('');
                        $('#password').val('');                        
                   """
        self.js_invoke(js_code)                 # this clears the values
        self.page.type('#username', username)   # this triggers the js events required
        self.page.type('#password', password)
        self.page.click('#signin_button')       # this submits the form
        self.wait(2)
        #self.page.wait_for_navigation()

    def logout(self):
        self.open('/console/logout!doLogout')


    def page_billing(self):
        self.open('/billing/home')

    def create_iam_user(self):

        # Create user and set password
        user_name = 'gw-bot-aws-user'
        password = '**********'                 # replace with good pwd
        user = IAM_User(user_name=user_name)
        user.create()
        user.set_password(password,reset_required=False)

        # add user the policy to read the billing data
        policy_arn = 'arn:aws:iam::aws:policy/job-function/Billing'
        user.iam.user_attach_policy(policy_arn)

