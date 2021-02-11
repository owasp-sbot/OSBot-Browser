def run(event, context=None):
    return f"From osbot_browser lambda code, hello {event.get('name')}"