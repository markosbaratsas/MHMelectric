from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# added to implement MyAuthentication class
from django.utils.translation import gettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# subbclass the TokenAuthentication class in order to fullfil the API's specifications
# with the custom HTTP_HEADER
class MyAuthentication(TokenAuthentication):
    keyword = "Whatever, since we don't use it!"

    # got this from `https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py`
    # and made some changes, so that we don't use the `keyword`
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth:
            return None

        if len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[0].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)


def get_authorization_header(request):

    # custom header `X-OBSERVATORY-AUTH` is used, as per specifications

    auth = request.META.get('HTTP_X_OBSERVATORY_AUTH', b'')
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth
