from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (str(user.pk) + str(timestamp)) + str(user.is_active)


member_activation_token = AccountActivationTokenGenerator()
