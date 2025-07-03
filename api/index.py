from django.core.wsgi import get_wsgi_application
from vercel_wsgi import handle_request

application = get_wsgi_application()

def handler(request, context):
    return handle_request(request, application)
