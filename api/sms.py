import os
import environ
from environ import ImproperlyConfigured
from project.settings import BASE_DIR
from twilio.rest import Client


class SMS:
    def __init__(self):
        env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
        self.account_sid = self.get_env(env, "TWILIO_SID", None)
        self.auth_token = self.get_env(env, "TWILIO_TOKEN", None)
        self.phone = self.get_env(env, "TWILIO_PHONE", None)

        if self.account_sid is None or self.auth_token is None and self.phone is None:
            print("Twilio credentials not found\nWill print to stdout instead")
            return

        self.client = Client(self.account_sid, self.auth_token)

    def send(self, phone, message):
        if not self.client:
            print(f"Redirected SMS to StdOut {phone}\n: {message}")
            return

        try:
            self.client.messages.create(from_=self.phone, to="+" + phone, body=message)
        except Exception as e:
            print(f"Error sending SMS to {phone}\n: {e}")
            print(f"Message: {message}")

        print(f"Redirected SMS to {phone}:\n {message}")

    def get_env(self, env: callable, name: str, default: any = None) -> str | None:
        """
        Get the environment variable
        :param env: environ Object, or Function
        :param name: Name of the environment variable
        :param default: Default value if the environment variable is not found
        :return: Value of the environment variable
        """
        try:
            value = env(name)
            value = value.strip()

            if value == "" and default:
                return default

            return value
        except ImproperlyConfigured:
            return default
