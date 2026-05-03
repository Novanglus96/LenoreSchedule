from ninja.security import HttpBearer
from decouple import config
from django.conf import settings


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        """
        The `authenticate` function authenticates the api endpoint.

        Args:
            request (HTTPRequest): The http request.
            token (): CSRF Token

        Returns:
            (dict): {'type': api_key, 'name': service-account}
        """
        api_key = getattr(settings, "VITE_API_KEY", None) or config(
            "VITE_API_KEY", default=None
        )

        if api_key and token == api_key:
            return {
                "type": "api_key",
                "name": "service-account",
            }


def get_user_divisions(request):
    """
    Returns the Division queryset the request's user is permitted to see,
    or ``None`` if the user has unrestricted access.

    Rules:
    - Unauthenticated (API-key / service account): ``None`` → unrestricted
    - ``is_staff`` or ``is_superuser``: ``None`` → unrestricted
    - Regular authenticated user: their profile's divisions queryset
    - Authenticated user with no profile: empty queryset → no access
    """
    from staff.models import Division

    user = request.user
    if not user.is_authenticated:
        return None
    if user.is_staff or user.is_superuser:
        return None
    try:
        return user.profile.divisions.all()
    except Exception:
        return Division.objects.none()
