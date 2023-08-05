from rest_framework import permissions

from sigauth.helpers import RequestSignatureChecker


class SignatureCheckPermissionBase(permissions.BasePermission):
    secret = None
    check_nonce = True

    def __init__(self, *args, **kwargs):
        self.request_checker = RequestSignatureChecker(self.secret)
        super().__init__(*args, **kwargs)

    def has_permission(self, request, view):
        return self.request_checker.test_signature(request, check_nonce=self.check_nonce)
