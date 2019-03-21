from time import sleep
from utils.Dev import Dev
from utils.Lambdas_Helpers import slack_message
from utils.Misc import Misc
from utils.aws.Lambdas import load_dependencies

gsuite_secret_id = 'gsuite_gsbot_user'

class Full_Calendar_Views:

    @staticmethod
    def _show_google_calendar(calendar_data,team_id=None, channel=None,headless=True):
        #load_dependencies(['syncer', 'requests', 'gmail']);
        from view_helpers.Full_Calendar import Full_Calendar

        full_calendar = Full_Calendar(headless=headless)
        full_calendar.load_page()

        events = []
        for event in calendar_data:
            start = event.get('start').get('date')
            end = event.get('end').get('date')
            if start is None:
                start = event.get('start').get('dateTime')
                end = event.get('end').get('dateTime')
            events.append({"title": event.get('summary'),
                           "start": start,
                           "end": end})

        Dev.pprint(events)
        # events = gcalendar.next_10()
        full_calendar.invoke_js('show_calendar', events)
        full_calendar.browser_width(1000, 700)
        return full_calendar.send_screenshot_to_slack(team_id=team_id, channel=channel)

    @staticmethod
    def gs_team(team_id=None, channel=None, params=None,headless=True):
        load_dependencies(['syncer', 'requests', 'gmail']);
        slack_message(":point_right: Loading data from GS Team shared calendar")
        from gsuite.GCalendar import GCalendar
        gcalendar = GCalendar(gsuite_secret_id=gsuite_secret_id)
        calendar_data = gcalendar.gs_team()
        return Full_Calendar_Views._show_google_calendar(calendar_data,team_id,channel)