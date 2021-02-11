from osbot_aws.apis.Lambda import Lambda
from osbot_aws.apis.shell.Lambda_Shell import Lambda_Shell
from osbot_aws.helpers.Lambda_Package import Lambda_Package
from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_utils.utils import Misc


class test_API_Browser_in_AWS(Test_Helper):

    def setUp(self):
        super().setUp()
        self.lambda_name = 'osbot_browser.lambdas.dev.browser_test'
        self._lambda = Lambda(self.lambda_name)
        self.api_browser_code = """
from osbot_aws.Dependencies import load_dependencies        
load_dependencies('syncer')        
from osbot_browser.browser.API_Browser import API_Browser        
api_browser = API_Browser()
"""

    def auth_key(self):
        return Lambda_Shell().get_lambda_shell_auth()

    def _invoke_shell_command(self, command, kwargs=None):
        params = {'lambda_shell': {'method_name': command , 'method_kwargs': kwargs , 'auth_key': self.auth_key()}}
        return self._lambda.invoke(params)

    def _invoke_python_code(self, code):
        code = self.api_browser_code + code
        return self._lambda.shell_python_exec(code, self.auth_key())

    def _invoke_python_line(self, line_of_code):
        code = self.api_browser_code + "result = " + line_of_code
        return self._lambda.shell_python_exec(code, self.auth_key())

    def _reset_lambda(self):
        Lambda_Package(self.lambda_name).reset()

    @group_by
    def _lambda_process_list(self):
        def parse_ps_aux(raw_data):

            import re
            regex = re.compile('[\s]+')
            lines = raw_data.split('\n')

            headers = regex.split(lines.pop(0))
            data = []
            for line in lines:
                item = {}
                for index, header in enumerate(headers):
                    values = regex.split(line)
                    item[header] = Misc.array_get(values, index)

                data.append(item)
            return data

        ps_aux = self._invoke_shell_command('list_processes')
        return parse_ps_aux(ps_aux)

    def _lambda_chrome_processes(self):
        return self._lambda_process_list(group_by='COMMAND').get('/tmp/lambdas-dependencies/pyppeteer/headless_shell')

    def _lambda_headless_shell_processes(self):
        return self._lambda_process_list(group_by='COMMAND').get('[headless_shell]')


    # test methods


    def test_update_lambda(self):
        self.result = Deploy().deploy_lambda__browser_dev(self.lambda_name)

    def test_ctor(self):
        assert self._invoke_python_line('api_browser.file_tmp_last_chrome_session')== '/tmp/browser-last_chrome_session.json'
        assert self._invoke_python_line('api_browser.headless'                    ) == True
        assert self._invoke_python_line('api_browser.new_browser'                 ) == False
        assert self._invoke_python_line('api_browser.log_js_errors_to_console'    ) == True


    def test_load_latest_version_of_chrome(self):
        self._reset_lambda()                                                                            # force lambda cold start
        headless_shell = '/tmp/lambdas-dependencies/pyppeteer/headless_shell'
        code_file_exists = f"""
from osbot_utils.utils.Files import file_exists
result = file_exists('{headless_shell}')
        """
        assert self._invoke_python_code(code_file_exists) is False                                      # check that file doesn't exist after cold start
        assert self._invoke_python_line('api_browser.load_latest_version_of_chrome()') is None          # trigger download of dependency
        assert self._invoke_python_code(code_file_exists) is True                                       # check that now it exists

    def test_sync__setup_browser(self):
        self._reset_lambda()
        code = """                 
from osbot_utils.utils.Files import file_contents             
load_dependencies('requests,pyppeteer,websocket-client')

api_browser.sync__setup_browser()
result = api_browser.get_last_chrome_session()
        """
        assert self._invoke_python_code(code).startswith('ws://127.0.0.1:')
        assert len(self._lambda_chrome_processes()) == 1 # there should only be one process

    def test_sync__setup_browser__new_browser__True(self):
        self._reset_lambda()
        code = """                 
from osbot_utils.utils.Files import file_contents             
load_dependencies('requests,pyppeteer,websocket-client')
api_browser.set_new_browser(True)
api_browser.sync__setup_browser()
result = api_browser.new_browser
        """
        self._invoke_python_code(code)
        assert len(self._lambda_chrome_processes()) == 1                # after call to sync__setup_browser, there should be 1 process
        self._invoke_python_code(code)
        assert len(self._lambda_chrome_processes()) == 2  # now there should be 2
        self._invoke_python_code(code)
        assert len(self._lambda_chrome_processes()) == 3  # now there should be 3
        self._reset_lambda()

        #print(self._invoke_shell_command('disk_space'    ))
        #print(self._invoke_shell_command('list_processes'))
        #print(self._invoke_shell_command('memory_usage'  ))
        #print(self._invoke_shell_command('file_contents' , {'path': '/var/runtime/lambda_runtime_client.py'}))

    def test_sync__screenshot(self):
        #self._reset_lambda()
        code = """                 
from osbot_utils.utils.Files import file_contents             
load_dependencies('requests,pyppeteer,websocket-client')

api_browser.sync__setup_browser()
#api_browser.sync__open('https://www.google.com/')
api_browser.sync__open('https://www.whatismybrowser.com/')

result = api_browser.sync__screenshot_base64()
"""
        self.png_data = self._invoke_python_code(code)

        #self.result = self._invoke_shell_command('list_processes')

