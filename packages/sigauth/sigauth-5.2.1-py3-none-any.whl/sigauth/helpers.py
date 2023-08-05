import logging
from urllib.parse import urlsplit

from mohawk import Receiver, Sender
from mohawk.exc import HawkFail
from rest_framework.exceptions import AuthenticationFailed
from django.core.cache import cache

NO_CREDENTIALS_MESSAGE = 'Authentication credentials were not provided.'
INCORRECT_CREDENTIALS_MESSAGE = 'Incorrect authentication credentials'

default_content_type = 'text/plain'
default_content = ''

logger = logging.getLogger(__name__)


class RequestSigner:
    algorithm = 'sha256'
    header_name = 'X-Signature'
    secret = None
    sender_id = None

    def __init__(self, secret, sender_id):
        self.secret = secret
        self.sender_id = sender_id

    def get_signature_headers(self, url, body, method, content_type):
        sender = Sender(
            {
                'id': self.sender_id,
                'key': self.secret,
                'algorithm': self.algorithm
            },
            get_path(url),
            method,
            content=get_content(body),
            content_type=get_content_type(content_type),
        )

        return {
            self.header_name: sender.request_header
        }


class RequestAuthorisationSigner:
    algorithm = 'sha256'
    header_name = 'authorization'
    secret = None
    sender_id = None

    def __init__(self, secret, sender_id):
        self.secret = secret
        self.sender_id = sender_id

    def get_signature_headers(self, url, body, method, content_type):
        sender = Sender(
            {
                'id': self.sender_id,
                'key': self.secret,
                'algorithm': self.algorithm
            },
            url,
            method,
            content=body,
            content_type=content_type,
        )

        return {
            self.header_name: sender.request_header
        }


class RequestSignatureChecker:

    header_name = 'HTTP_X_SIGNATURE'
    authorisation_header_name = 'HTTP_AUTHORIZATION'
    secret = None
    algorithm = 'sha256'

    def __init__(self, secret):
        self.secret = secret

    def lookup_credentials(self, sender_id):
        return {
            'id': sender_id,
            'key': self.secret,
            'algorithm': self.algorithm
        }

    def test_signature(self, request, **kwargs):
        """
        Thest that the signature header matches the expected value.

        Args
            request (django.http.Request): The request to check the properties.
        Returns:
            bool or Receiver : False if rejected, Receiver instance if accepted

        """
        check_nonce = kwargs.get("check_nonce")
        if self.header_name in request.META:
            # HTTP_X_SIGNATURE is present check using this method
            return self.test_hawk_signature(request, check_nonce=check_nonce)
        elif self.authorisation_header_name in request.META:
            # HTTP_AUTHORIZATION is present check using this method
            return self.test_hawk_authorisation(request)
        else:
            # No Authorisation header present
            raise AuthenticationFailed(NO_CREDENTIALS_MESSAGE)

    def test_hawk_authorisation(self, request):
        try:
            return Receiver(
                self.lookup_credentials,
                request.META[self.authorisation_header_name],
                request.build_absolute_uri(),
                request.method,
                content=request.body,
                content_type=request.content_type,
                seen_nonce=seen_nonce,
            )
        except HawkFail as e:
            logger.warning(
                'Failed authentication {e}'.format(
                    e=e,
                )
            )
            raise AuthenticationFailed(INCORRECT_CREDENTIALS_MESSAGE)

    def test_hawk_signature(self, request, check_nonce=True):

        content_type = get_content_type(request.META.get('CONTENT_TYPE'))
        receiver_kwargs = {
            "content": get_content(request.body),
            "content_type": get_content_type(content_type),
        }
        if check_nonce:
            receiver_kwargs.update({"seen_nonce": seen_nonce})
        try:
            content_type = get_content_type(request.META.get('CONTENT_TYPE'))
            return Receiver(
                self.lookup_credentials,
                request.META.get(self.header_name),
                request.get_full_path(),
                request.method,
                **receiver_kwargs
            )
        except HawkFail as e:
            logger.warning(
                'Failed authentication {e}'.format(
                    e=e,
                )
            )
            raise AuthenticationFailed(INCORRECT_CREDENTIALS_MESSAGE)


def get_path(url):
    """
    Get the path from a given url, including the querystring.

    Args:
        url (str)
    Returns:
        str

    """

    url = urlsplit(url)
    path = url.path
    if url.query:
        path += "?{}".format(url.query)
    return path


def get_content_type(content_type):
    return default_content_type if content_type is None else content_type


def get_content(content):
    return default_content if content is None else content


def seen_nonce(access_key_id, nonce, _):
    """Returns if the passed access_key_id/nonce combination has been
    60 seconds is a skew in either direction, not just the past.
    Hence a 120 second window in which a request could be replayed
    """
    cache_key = 'hawk_authentication:{access_key_id}:{nonce}'.format(
        access_key_id=access_key_id,
        nonce=nonce,
    )

    # cache.add only adds key if it isn't present
    seen_cache_key = not cache.add(
        cache_key,
        True,
        timeout=120,
    )

    if seen_cache_key:
        logger.warning('Already seen nonce {nonce} via sigauth'.format(nonce=nonce))

    return seen_cache_key
