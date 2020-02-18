from osbot_aws.helpers.Lambda_Package import Lambda_Package
from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.Deploy              import Deploy
from osbot_browser.lambdas.jira_web import run


class test_jira_web(Test_Helper):
    def setUp(self):
        super().setUp()
        self.png_data = None
        self.result = None
        self.aws_lambda = Lambda_Package('osbot_browser.lambdas.jira_web')

    def test_update_lambda(self):
        Deploy().setup().deploy_lambda__browser('osbot_browser.lambdas.jira_web')

    def test_update_lambda_code(self):
        from gw_bot.setup.OSS_Setup import OSS_Setup
        OSS_Setup().lambda_package('osbot_browser.lambdas.jira_web').aws_lambda.reset()

    def test_invoke_directly(self):
        issue_id = 'VP-2'
        payload = { 'issue_id' : issue_id , 'channel': 'DRE51D4EM' , 'delay': 0}
        self.result = run(payload,{})

    def test_invoke_lambda(self):
        self.test_update_lambda()
        payload = {}
        self.png_data = self.aws_lambda.invoke(payload)

    def test_invoke_lambda__screenshot(self):
        self.test_update_lambda()
        issue_id = 'VP-1'
        payload = {'issue_id': issue_id, 'channel': 'DRE51D4EM', 'delay': 6}
        self.result = self.aws_lambda.invoke(payload)

    def test_invoke(self):

        self.test_update_lambda()
        issue_id = 'PERSON-42'

        payload = { 'issue_id': issue_id   ,
                    #'channel': 'DRE51D4EM' ,            # gwbot
                    'width'  : 1200,
                    'height' : 300 ,
                    'wait'   : 2   }
        self.png_data = self.aws_lambda.invoke(payload)

    def test_send_to_slack(self):
        team_id = None
        channel = 'DRE51D4EM'
        issue_id = 'Person-42'
        png_data = "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8" \
                   "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
        title = "Issue: {0}".format(issue_id)
        Browser_Lamdba_Helper().send_png_data_to_slack(team_id, channel, title, png_data)

