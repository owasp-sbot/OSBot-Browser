from time import sleep

from utils.Dev import Dev
from utils.Misc import Misc
from utils.aws.Lambdas import load_dependencies
from view_helpers.Full_Calendar import Full_Calendar


class Full_Calendar_Views:

    @staticmethod
    def default(team_id=None, channel=None, params=None,headless=True):
        calendar = Full_Calendar(headless=headless)
        calendar.load_page()

        return calendar.send_screenshot_to_slack()