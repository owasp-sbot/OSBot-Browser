from osbot_aws.helpers.Lambda_Package import Lambda_Package
from osbot_utils.utils.Files import path_combine


class Deploy:
    def __init__(self, lambda_name):
        self.package         = Lambda_Package(lambda_name)      # refactor to use Deploy Lambda
        self.tmp_s3_bucket = 'gs-lambda-tests'
        self.tmp_s3_key    = 'gsbot/{0}.zip'.format(lambda_name)
        self.setup()

    def setup(self):
        (self.package.aws_lambda.set_s3_bucket(self.tmp_s3_bucket)
                             .set_s3_key   (self.tmp_s3_key))
        return self

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
        return package


    def deploy_lambda__browser_dev(self, lambda_name):
        #package = self.get_package(lambda_name)
        package = self.package
        source_folder = path_combine(__file__, '../osbot_browser')  # to do check path
        #package.add_module('osbot_browser')
        package.add_folder(source_folder, ignore='web_root')
        package.add_module('osbot_aws')
        package.add_module('osbot_utils')
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