from osbot_aws.apis.Lambda import load_dependencies
from osbot_gsuite.apis.GCalendar import GCalendar

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message

gsuite_secret_id = 'gsuite_gsbot_user'

class Full_Calendar_Views:

    @staticmethod
    def _get_gcalendar():
        load_dependencies(['syncer', 'requests', 'gmail']);
        return GCalendar(gsuite_secret_id=gsuite_secret_id)

    @staticmethod
    def _show_google_calendar(calendar_data,team_id=None, channel=None,headless=True):
        #load_dependencies(['syncer', 'requests', 'gmail']);
        from osbot_browser.view_helpers.Full_Calendar import Full_Calendar

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
        slack_message(":point_right: Loading data from GS Team shared calendar", [], channel,team_id)

        calendar_data = Full_Calendar_Views._get_gcalendar().gs_team()
        return Full_Calendar_Views._show_google_calendar(calendar_data,team_id,channel)

    @staticmethod
    def gs_cs_team(team_id=None, channel=None, params=None, headless=True):
        slack_message(":point_right: Loading data from GS CS Team shared calendar", [], channel, team_id)

        calendar_data = Full_Calendar_Views._get_gcalendar().gs_cs_team()

        return Full_Calendar_Views._show_google_calendar(calendar_data, team_id, channel)