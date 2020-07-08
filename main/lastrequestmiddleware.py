from django.utils.timezone import now
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import InvalidToken
from main import models


class LastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # try to get user by jwt token
        # except get user from request
        try:
            user = authentication.JWTAuthentication().authenticate(request)[0]
        except (InvalidToken, TypeError):
            user = request.user

        if user.is_authenticated:
            user_act = models.UserActivity.objects.filter(user=user)[0]
            user_act.last_request_date = now()
            user_act.save()
