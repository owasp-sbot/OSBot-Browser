from osbot_browser.browser.Browser_Commands import load_dependencies

def run(event, context):
    load_dependencies('syncer,requests,pyppeteer')
    from osbot_browser.view_helpers.Google_Charts_Js import Google_Charts_Js
    google_charts = Google_Charts_Js()
    google_charts.load_page(True)
    chart_type = event.get('chart_type')
    options    = event.get('options'   )
    width      = event.get('width'     )
    height     = event.get('height'    )
    data       = event.get('data'      )
    clip       = event.get('clip'      )
    png_data = google_charts.create_chart(chart_type, options, width, height, data, clip)
    return png_data