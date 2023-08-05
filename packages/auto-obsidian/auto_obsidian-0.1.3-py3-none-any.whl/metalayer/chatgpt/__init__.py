USE_SERVER = True

if USE_SERVER:
    from .chatgpt_server import complete, complete_async
else:
    from .chatgpt import complete, complete_async
