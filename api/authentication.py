from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.exceptions import AuthenticationFailed
from firebase_admin import auth as firebase_auth
from api.models import User

class FirebaseAuthentication(authentication.BaseAuthentication):
    """
    "Authorization" HTTP header, preprended with the string "<keyword> " where
    <keyword> is this classes `keyword` string property. For example:
    Authorization: xxxxx.yyyyy.zzzzz
    """

    check_revoked = False

    def authenticate(self, request):

        auth = authentication.get_authorization_header(request)

        try:
            firebase_token = auth.decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise AuthenticationFailed(msg)

        return self._authenticate_credentials(firebase_token)

    def _authenticate_credentials(self, firebase_token):

        try:
            print(firebase_token)
            decoded_token = firebase_auth.verify_id_token(
                firebase_token,
                check_revoked=self.check_revoked
            )
        except firebase_auth.InvalidIdTokenError:
            msg = 'Auth token is invalid.'
            raise AuthenticationFailed(msg)
        except firebase_auth.ExpiredIdTokenError:
            msg = 'Auth token is expired.'
            raise AuthenticationFailed(msg)
        except firebase_auth.RevokedIdTokenError:
            msg = 'Auth token is been revoked.'
            raise AuthenticationFailed(msg)
        except firebase_auth.CertificateFetchError:
            msg = 'Temporarily unable to verify the ID token.'
            raise AuthenticationFailed(msg)

        return get_user_model().objects.get_or_create(
            email=decoded_token['email'],
            id=decoded_token['uid']            
        )
