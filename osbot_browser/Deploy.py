import os

from osbot_aws.deploy.Deploy_Lambda import Deploy_Lambda
from osbot_aws.helpers.Lambda_Package import Lambda_Package
from osbot_utils.utils.Files import path_combine


class Deploy:
    def __init__(self, handler):
        self.deploy_lambda = Deploy_Lambda(handler)
        self.deploy_lambda.package.aws_lambda.runtime = 'python3.7'

    def configure_environment_variables(self):
        vars_to_add = ['OSBOT_LAMBDA_S3_BUCKET','OSBOT_LAMBDA_S3_FOLDER_LAMBDAS']
        env_variables = {}
        for var_to_add in vars_to_add:
            env_variables[var_to_add] = os.environ.get(var_to_add)

        self.update_environment_variables(env_variables)

    def update_environment_variables(self, env_variables):
        aws_lambda = self.deploy_lambda.package.aws_lambda
        aws_lambda.env_variables = env_variables
        aws_lambda.update_lambda_configuration()

    def deploy_lambda__browser(self, lambda_name='osbot_browser.lambdas.lambda_browser'):
        #package = self.get_package(lambda_name)
        #source_folder = path_combine(__file__, '../../modules/OSBot-browser/osbot_browser')
        #package.add_folder(source_folder)
        #gw_bot_folder = path_combine(__file__,'../../gw_bot')  # this is needed because of some of the helpers (which will need to be refactored into a separate module)
        #package.add_folder(gw_bot_folder)
        package = self.package
        package.add_module('osbot_browser')
        package.add_module('osbot_aws')
        package.add_osbot_utils()
        package.update()
        self.configure_environment_variables()
        return package


    def deploy_lambda__browser_dev(self):
        #package = self.get_package(lambda_name)
        package = self.deploy_lambda.package
        source_folder = path_combine(__file__, '../../osbot_browser')  # to do check path
        #package.add_module('osbot_browser')
        package.add_folder(source_folder, ignore='web_root')
        #package.add_osbot_utils()
        package.add_osbot_aws()
        self.configure_environment_variables()
        package.update()
        return package
    # don't use this version (on the OSS Fork)
    # def deploy(self, delete_before=False):
    #     if delete_before:
    #         self.package.delete()
    #     code_folder = Files.path_combine(__file__,'..')
    #     self.package.add_folder(code_folder)
    #     self.package.add_root_folder()
    #     self.package.add_pbx_gs_python_utils()
    #     #Dev.pprint(self.package.get_files())
    #     return self.package.update()