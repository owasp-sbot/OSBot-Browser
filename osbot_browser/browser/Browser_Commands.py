import json

from osbot_aws.apis.Lambda                                  import Lambda
from osbot_browser.browser.Browser_Lamdba_Helper            import Browser_Lamdba_Helper
from pbx_gs_python_utils.utils.Files                        import Files
from pbx_gs_python_utils.utils.Lambdas_Helpers              import slack_message
from pbx_gs_python_utils.utils.Misc                         import Misc
from pbx_gs_python_utils.utils.Process                      import Process
from pbx_gs_python_utils.utils.slack.Slack_Commands_Helper  import Slack_Commands_Helper


def load_dependency(target):
    from osbot_aws.apis.S3 import S3
    import shutil
    import sys
    s3         = S3()
    s3_bucket  = 'gw-bot-lambdas'
    s3_key     = 'lambdas-dependencies/{0}.zip'.format(target)
    tmp_dir    = Files.path_combine('/tmp/lambdas-dependencies', target)
    #return s3.file_exists(s3_bucket,s3_key)

    if s3.file_exists(s3_bucket,s3_key) is False:
        raise Exception("In Lambda load_dependency, could not find dependency for: {0}".format(target))

    if Files.not_exists(tmp_dir):                               # if the tmp folder doesn't exist it means that we are loading this for the first time (on a new Lambda execution environment)
        zip_file = s3.file_download(s3_bucket, s3_key,False)    # download zip file with dependencies
        shutil.unpack_archive(zip_file, extract_dir = tmp_dir)  # unpack them
        sys.path.append(tmp_dir)                                # add tmp_dir to the path that python uses to check for dependencies
    return Files.exists(tmp_dir)

class Browser_Commands:

    current_version = 'v0.41 (gw)'

    @staticmethod
    def oss_today(team_id=None, channel=None, params=[]):

        # here is the jscode tha cleans up the oss schedule ui
        js_code = """$('.inner_main_schedule').height(130)
                     $('.center_heading').height(-50)     
                     $('footer').hide()                   
                     $('.edit-link').hide()               
                     $('#no-room-booked').hide() 
                     $('#schedule-by-day').hide()
                     $('#Villas #AM_1').hide()
                     $('#Villas #PM_1').hide()
                     $('#Villas #PM_2').hide()          
                     $('#Villas #PM_3').hide()                                                   
                     $('#Main_conference_Hall #DS_1').hide()                     
                     $('#Main_conference_Hall #DS_3').hide()"""


        load_dependency('syncer');
        load_dependency('requests')
        load_dependency('pyppeteer')
        url = 'https://opensecsummit.org/schedule/day/fri/'
        from osbot_browser.browser.Browser_Page import Browser_Page
        page = Browser_Page(headless=True, new_page=True).setup()
        page.open(url).width(1200)
        page.javascript_eval(js_code)

        png_data = page.screenshot()
        return page.browser_helper.send_png_data_to_slack(team_id, channel, url, png_data)


    @staticmethod
    def slack(team_id=None, channel=None, params=None):


        target    = Misc.array_pop(params,0)
        height    = Misc.to_int(Misc.array_pop(params, 0))
        width     = Misc.to_int(Misc.array_pop(params, 0))
        scroll_by = Misc.to_int(Misc.array_pop(params, 0))
        delay     = Misc.to_int(Misc.array_pop(params, 0))

        if target    is None: target = 'general'
        if width     is None: width = 800
        if height    is None: height = 1000
        if scroll_by is None: scroll_by = 0
        if delay     is None: delay = 0

        target_url = '/messages/{0}'.format(target)

        slack_message(":point_right: Taking screenshot of slack channel: `{0}` with height `{1}`, width `{2}`, scroll_by `{3}` and delay `{4}`".format(target, height,width,scroll_by,delay), [], channel, team_id)

        payload = {'target'    : target_url,
                   'channel'   : channel,
                   'team_id'   : team_id,
                   'width'     : width,
                   'height'    : height,
                   'scroll_by' : scroll_by,
                   'delay'     : delay}
        aws_lambda      = Lambda('osbot_browser.lambdas.slack_web')
        aws_lambda.invoke_async(payload)

        #browser_helper  = Browser_Lamdba_Helper()
        #return browser_helper.send_png_data_to_slack(team_id, channel, target, png_data)


    @staticmethod
    def screenshot(team_id=None, channel=None, params=[]):
        load_dependency('syncer');
        load_dependency('requests')
        load_dependency('pyppeteer')

        url            = params.pop(0).replace('<', '').replace('>', '')  # fix extra chars added by Slack
        width          = Misc.to_int(Misc.array_pop(params,0))
        height         = Misc.to_int(Misc.array_pop(params,0))
        delay          = Misc.to_int(Misc.array_pop(params, 0))
        message = ":point_right: taking screenshot of url: {0}".format(url)
        if width : message += ", with width `{0}`".format(width)
        if height: message += ", with height `{0}` (min height)".format(height)
        if delay : message += ", with delay of  `{0}` seconds".format(delay)
        slack_message(message,[], channel,team_id)

        browser_helper = Browser_Lamdba_Helper().setup()
        if width:
            browser_helper.api_browser.sync__browser_width(width,height)
        png_data       = browser_helper.get_screenshot_png(url,full_page=True,delay=delay)
        return browser_helper.send_png_data_to_slack(team_id,channel,url, png_data)

    @staticmethod
    def lambda_status(team_id, channel, params):
        text        = "Here are the current status of the `graph` lambda function"
        attachments = [ { 'title':'Processes','text'  : Process.run("ps", ["-A"]        ).get('stdout') },
                        {'title': 'Temp Files', 'text': Process.run("ls", ["-ls",'/tmp']).get('stdout') }]
        return text,attachments

    @staticmethod
    def list(team_id, channel, params):
        text = "Here are the current examples files:"
        attachments = []
        files       = ''
        web_root    = Browser_Lamdba_Helper().web_root() +'/'
        for file in Files.files(web_root):
            files += '{0} \n'.format(file.replace(web_root,''))
        attachments.append({'text': files })
        return text, attachments

    @staticmethod
    def markdown(team_id, channel, params):
        path  = 'examples/markdown.html'
        js_code = {'name': 'convert', 'params': '# Markdown code!!! \n 123 \n - bullet point \n - another one ![](http://visjs.org/images/gettingstartedSlide.png)'}
        if params and len(params) > 0:
            js_code['params']= ' '.join(params).replace('```','')

        return Browser_Lamdba_Helper().setup()                                   \
                                      .render_file(team_id, channel, path,js_code)

    @staticmethod
    def render(team_id, channel, params):
        load_dependency('syncer');
        load_dependency('requests')
        load_dependency('pyppeteer')
        if params:
            target = params.pop(0)
            delay  = Misc.to_int(Misc.array_pop(params,0))
            if len(params) == 4:
                clip = {'x': int(params[0]), 'y': int(params[1]), 'width': int(params[2]), 'height': int(params[3])}
            else:
                clip = None
        else:
            return None

        slack_message(":point_right: rendering file `{0}`".format(target), [], channel, team_id)
        return Browser_Lamdba_Helper().setup().render_file(team_id, channel, target,clip=clip, delay=delay)

        #png_file = browser_helper.render_page.screenshot_file_in_folder(browser_helper.web_root(), target, clip=clip)
        #return browser_helper.send_png_file_to_slack(team_id, channel, target, png_file)

        # return None
        # load_dependency('syncer')
        # load_dependency('requests')
        # from osbot_browser.browser.API_Browser import API_Browser
        # from osbot_browser.browser.Render_Page import Render_Page
        #
        # web_root = './web_root/'
        # target   = url_path
        #
        # api_browser = API_Browser().sync__setup_browser()
        # render_page = Render_Page(api_browser)
        #
        # browser_helper = Browser_Lamdba_Helper().setup()
        # png_file = render_page.screenshot_file_in_folder(web_root, target, clip=clip)
        #
        # return browser_helper.send_png_file_to_slack(team_id, channel, 'markdown', png_file)
        # #return Browser_Commands._send_to_slack__png_file(team_id, channel, target, png_file)

    # @staticmethod
    # def risks(team_id=None, channel=None, params=None):
    #     path = '/gs/risk/r1-and-r2.html'
    #     data = {}
    #     if params and len(params) > 0:
    #         fixed_params = ' '.join(params).replace('```','')
    #         data = {}
    #         for items in fixed_params.split(','):
    #             values = items.split(':')
    #             data[values[0].strip()] = values[1].strip()
    #
    #     js_code = "r1_and_r2.set_risks({0})".format(json.dumps(data))
    #     clip = {'x': 1, 'y': 1, 'width': 915, 'height': 435}
    #     browser = Browser_Lamdba_Helper().setup()
    #     return browser.render_file(team_id, channel, path=path, js_code=js_code, clip=clip)

        #return browser.open_local_page_and_get_screenshot(path, js_code=js_code, png_file=png_file)

        #
        #.set_risks({'r1_2': '1', 'r2_4': '0', 'r5_4': '2'})

    @staticmethod
    def risks(team_id=None, channel=None, params=None):
        load_dependency('syncer') ;
        load_dependency('requests')

        from osbot_browser.view_helpers.Risk_Dashboard import Risk_Dashboard

        jira_key = params.pop(0)

        return ( Risk_Dashboard().create_dashboard_for_jira_key(jira_key)
                                 .send_graph_name_to_slack(team_id, channel)
                                 .send_screenshot_to_slack(team_id, channel))

        # graph_name = 'graph_DGK'
        # root_node = 'GSSP-6'
        #
        # return Risk_Dashboard().create_dashboard_for_graph(graph_name,root_node).send_screenshot_to_slack(team_id, channel)


    @staticmethod
    def risks_test_data(team_id=None, channel=None, params=None):
        load_dependency('syncer') ;
        load_dependency('requests')

        from osbot_browser.view_helpers.Risk_Dashboard import Risk_Dashboard

        return Risk_Dashboard().create_dashboard_with_test_data().send_screenshot_to_slack(team_id, channel)

        #browser = Risk_Dashboard().create_dashboard_with_test_data().browser()

        #clip = {'x': 1, 'y': 1, 'width': 915, 'height': 435}
        #png_file =  browser.sync__screenshot(clip = clip)
        #return Browser_Lamdba_Helper().send_png_file_to_slack(team_id, channel, 'markdown', png_file)


    @staticmethod
    def vis_js(team_id=None, channel=None, params=None):
        path = 'examples/vis-js.html'

        params = ' '.join(params).replace('“','"').replace('”','"')
        data = json.loads(params)

        load_dependency('syncer')
        load_dependency('requests')

        nodes   = data.get('nodes'  )
        edges   = data.get('edges'  )
        options = data.get('options')
        from osbot_browser.view_helpers.Vis_Js import Vis_Js
        vis_js = Vis_Js()
        vis_js.create_graph(nodes, edges, options)
        #vis_js.show_jira_graph(graph_name)
        return vis_js.send_screenshot_to_slack(team_id,channel)

        # browser = Browser_Lamdba_Helper().setup()
        #
        # return browser.open_local_page_and_get_html(path,js_code=js_code)

        #return browser.render_file(team_id, channel,path, js_code=js_code)


    @staticmethod
    def am_charts(team_id=None, channel=None, params=None):
        if len(params) < 2:
            text = ':red_circle: Hi, for the `am_charts` command, you need to provide 2 parameters: '
            attachment_text = '*graph name* - the nodes and edges you want to view\n' \
                              '*view name* - the view to render'
            return text, [{'text': attachment_text}]

        from osbot_browser.view_helpers.Am_Charts_Views import Am_Charts_Views
        params[0], params[1] = params[1], params[0]

        (text, attachments) = Slack_Commands_Helper(Am_Charts_Views).show_duration(True).invoke(team_id, channel, params)

        if team_id is None:
            return text

    @staticmethod
    def calendar(team_id=None, channel=None, params=None):
        from osbot_browser.view_helpers.Full_Calendar_Views import Full_Calendar_Views
        #params[0], params[1] = params[1], params[0]
        Slack_Commands_Helper(Full_Calendar_Views).show_duration(True).invoke(team_id, channel,params)


    @staticmethod
    def go_js(team_id=None, channel=None, params=None):
        if len(params) < 2:
            text = ':red_circle: Hi, for the `go_js` command, you need to provide 2 parameters: '
            attachment_text = '*graph name* - the nodes and edges you want to view\n' \
                              '*view name* - the view to render'
            return text, [{'text': attachment_text}]

        from osbot_browser.view_helpers.Go_Js_Views import Go_Js_Views
        params[0], params[1] = params[1], params[0]

        (text, attachments) = Slack_Commands_Helper(Go_Js_Views).show_duration(True).invoke(team_id, channel, params)

        if team_id is None:
            return text

    @staticmethod
    def graph(team_id=None, channel=None, params=None):
        if len(params) < 2:
            text = ':red_circle: Hi, for the `graph` command, you need to provide 2 parameters: '
            attachment_text = '*graph name* - the nodes and edges you want to view\n' \
                              '*view name* - the view to render'
            return text,[{'text': attachment_text}]

        from osbot_browser.view_helpers.Vis_Js_Views import Vis_Js_Views

        params[0],params[1] = params[1],params[0]       # swap items (since it is more user friendly to add the graph name first)

        (text, attachments) = Slack_Commands_Helper(Vis_Js_Views).show_duration(False).invoke(team_id, channel, params)

        if team_id is None:
            return text

    @staticmethod
    def viva_graph(team_id=None, channel=None, params=None):
        if len(params) < 2:
            text = ':red_circle: Hi, for the `viva_graph` command, you need to provide 2 parameters: '
            attachment_text = '*graph name* - the nodes and edges you want to view\n' \
                              '*view name* - the view to render'
            return text, [{'text': attachment_text}]

        from osbot_browser.view_helpers.VivaGraph_Js_Views import VivaGraph_Js_Views

        params[0], params[1] = params[1], params[0]

        (text, attachments) = Slack_Commands_Helper(VivaGraph_Js_Views).show_duration(True).invoke(team_id, channel, params)

        if team_id is None:
            return text

    @staticmethod
    def elk(team_id=None, channel=None, params=None):
        load_dependency('syncer')
        from osbot_browser.browser.sites.Site_ELK import ELK_Commands
        from osbot_browser.browser.sites.Site_ELK import Site_ELK

        if len(params) == 0:
            Slack_Commands_Helper(ELK_Commands).invoke(team_id, channel, params)
            return None

        browser_helper = Browser_Lamdba_Helper().setup()
        elk = Site_ELK(browser_helper.api_browser, team_id, channel)

        elk.sync__connect_and_login()

        params.append(browser_helper)
        params.append(elk)

        result = Slack_Commands_Helper(ELK_Commands).invoke(team_id, channel, params)

        if team_id:
            return None
        else:
            return result

    @staticmethod
    def table(team_id=None, channel=None, params=None):

        if len(params) < 2:
            text = ':red_circle: Hi, for the `table` command, you need to provide 2 parameters: '
            attachment_text = '*target* - the jira id or graph to get\n' \
                              '*view name* - the view to render'
            return text,[{'text': attachment_text}]

        from osbot_browser.view_helpers.DataTable_Js_Views import DataTable_Js_Views

        params[0],params[1] = params[1],params[0]       # swap items (since it is more user friendly to add the graph name first)

        (text, attachments) = Slack_Commands_Helper(DataTable_Js_Views).show_duration(False).invoke(team_id, channel, params)

        if team_id is None:
            return text





    @staticmethod
    def maps(team_id=None, channel=None, params=None):
        load_dependency('syncer')
        load_dependency('requests')
        load_dependency('pyppeteer')
        from osbot_browser.view_helpers.Maps_Views import Maps_Views
        (text,attachments) = Slack_Commands_Helper(Maps_Views).invoke('not-used', channel, params)
        if team_id is None:
            return text

    @staticmethod
    def sow(team_id=None, channel=None, params=None):
        load_dependency('syncer')
        load_dependency('requests')
        load_dependency('pyppeteer')
        from osbot_browser.view_helpers.Sow_Views import Sow_Views
        (text, attachments) = Slack_Commands_Helper(Sow_Views).invoke('not-used', channel, params)
        if team_id is None:
            return text


    @staticmethod
    def version(team_id=None, channel=None, params=None):
        return Browser_Commands.current_version