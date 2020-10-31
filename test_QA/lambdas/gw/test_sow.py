from osbot_aws.apis.Lambda import Lambda
from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_browser.lambdas.gw.sow import run, get_issue_data
from gw_bot.Deploy import Deploy

class test_sow(Test_Helper):
    def setUp(self):
        super().setUp()
        self.lambda_name = 'osbot_browser.lambdas.gw.sow'
        self.aws_lambda  = Lambda(self.lambda_name)
        self.result      = None
        self.png_data    = None

    def tearDown(self):
        super().print(self.result)
        super().save_png(self.png_data, '/tmp/lambda_png_file.png')

    def test_update_lambda(self):
        Deploy().setup().deploy_lambda__browser(self.lambda_name)



    def test_get_issue_data(self):
        issue_id = 'SOW-135'
        self.result = get_issue_data(issue_id)

    def test__invoke_in_lambda(self):
        self.test_update_lambda()
        issue_id = 'SOW-121'
        payload = { "issue_id" : issue_id }
        self.result = self.aws_lambda.invoke(payload)


    def test_invoke_lambda(self):
        issue_id = 'SOW-135'
        lambda_name = 'osbot_browser.lambdas.gw.sow'
        png_data = Lambda(lambda_name).invoke({'issue_id': issue_id})


    def test_invoke_directly(self):
        issue_id = 'SOW-129'
        payload = {"headless": False, "issue_id": issue_id}
        self.png_data = run(payload, None)



    def render_and_save(self, issue_id, title, target_folder):
        png_data = run({"issue_id": issue_id},{})
        target_file = f'{target_folder}/{issue_id} - {title}.png'
        super().save_png(png_data, target_file)

    def test_create_report_files(self):
        target = '/tmp/SOW_Items'
        issues_id = {
            #'SOW-119':  'A. Enable the ability to validate file type ' ,
            #'SOW-122': 'B. Develop a content-based dirty word tagging' ,
            #'SOW-126': 'C. Enable the ability to encode, insert, extract, and decode security features ',
            'SOW-129': 'D. Enable support of other file types',
            #'SOW-135': 'E. Develop support for multi-threaded execution.',
                      }
        for issue_id, title in issues_id.items():
            self.render_and_save(issue_id,title, target)

























