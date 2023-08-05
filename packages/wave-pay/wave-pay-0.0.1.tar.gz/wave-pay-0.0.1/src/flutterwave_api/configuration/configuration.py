import flutterwave_api
from flutterwave_api.exceptions import ConfigurationError
import flutterwave_api._http


class Configuration:

    timeout = None
    public_key = None
    secret_key = None

    def __init__(self, secret_key, public_key, **kwargs):
        if secret_key == "":
            raise ConfigurationError("Missing Secret key")
        if public_key == "":
            raise ConfigurationError("Missing Public key")
        self.secret_key = secret_key
        self.public_key = public_key
        self.timeout = kwargs.get("timeout", 60)

    @staticmethod
    def configure(secret_key, public_key, **kwargs):
        Configuration.secret_key = secret_key
        Configuration.public_key = public_key
        Configuration.timeout = kwargs.get("timeout", 60)

    @staticmethod
    def instantiate():
        return Configuration(
            secret_key=Configuration.secret_key,
            public_key=Configuration.public_key,
            timeout=Configuration.timeout
        )

    @staticmethod
    def gateway():
        return flutterwave_api.WaveGateway(config=Configuration.instantiate())

    def http(self):
        return flutterwave_api._http.Http(secret_key=self.secret_key, timeout=self.timeout)
