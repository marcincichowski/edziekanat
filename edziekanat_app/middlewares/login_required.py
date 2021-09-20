from django.http import HttpResponseRedirect
from django.urls import resolve, reverse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from edziekanat import settings


class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings by setting a tuple of routes to ignore
    """

    def process_request(self, request):
        assert hasattr(request, 'user'), """
        The Login Required middleware needs to be after AuthenticationMiddleware.
        Also make sure to include the template context_processor:
        'django.contrib.auth.context_processors.auth'."""
        current_route_name = str(resolve(request.path_info).route).strip('^').strip('/$')
        if not request.user.is_authenticated:
            if current_route_name == 'admin/login': return
            if not current_route_name in settings.AUTH_EXEMPT_ROUTES:
                return redirect(settings.AUTH_LOGIN_ROUTE)

        elif resolve(request.path_info).url_name in settings.AUTH_EXEMPT_ROUTES:
            if current_route_name == 'admin/login': return
            return HttpResponseRedirect('/')

