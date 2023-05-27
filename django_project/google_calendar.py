from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from google.oauth2 import service_account

class GoogleCalendarInitView(TemplateView):
    template_name = 'google_calendar_init.html'
    def get(self, request):
        credentials, _ = service_account.Credentials.from_service_account_file(
            'credentials.json',
            subject='[Your email address]',
        )
        authorization_url = credentials.get_authorization_url()
        return HttpResponseRedirect(authorization_url)

class GoogleCalendarRedirectView(TemplateView):
    template_name = 'google_calendar_redirect.html'
    def get(self, request):
        code = request.GET['code']
        credentials, _ = service_account.Credentials.from_authorized_user_info(
            credentials,
            code,
        )
        events = credentials.get_calendar_events()
        return render(request, self.template_name, {'events': events})