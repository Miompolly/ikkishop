from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """
        Override the default _make_hash_value to generate token without using last_login.
        """
        return (
            str(user.pk) + user.email +
            str(timestamp) + str(user.is_active)
        )

default_token_generator = CustomTokenGenerator()