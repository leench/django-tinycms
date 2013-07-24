from django.conf import settings
from django.core.urlresolvers import reverse

class SWFUploadMiddleware(object):
    def process_request(self, request):
        if (request.method == 'POST') and (request.path == reverse('tinycms.views.upload')):
            if request.POST.has_key(settings.SESSION_COOKIE_NAME):
                session_key = request.POST[settings.SESSION_COOKIE_NAME]
                request.COOKIES[settings.SESSION_COOKIE_NAME] = session_key
            if request.POST.has_key('csrfmiddlewaretoken'):
                request.COOKIES[settings.CSRF_COOKIE_NAME] = request.POST['csrfmiddlewaretoken']

