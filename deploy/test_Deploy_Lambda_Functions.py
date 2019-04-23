import unittest
from unittest import TestCase

from osbot_browser.Deploy import Deploy
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message


class test_Deploy_Lambda_Functions(TestCase):

    def test_deploy_lambda_functions(self):
        targets = [
                    'osbot_browser.lambdas.lambda_browser'    ,
                   ]
        result = ""
        for target in targets:
            Deploy(target).deploy()
            result += " • {0}\n".format(target)

        text        = ":hotsprings: [osbot-gsuite] updated lambda functions"
        attachments = [{'text': result, 'color': 'good'}]
        slack_message(text, attachments)  # gs-bot-tests
        Dev.pprint(text, attachments)


if __name__ == '__main__':
    unittest.main()