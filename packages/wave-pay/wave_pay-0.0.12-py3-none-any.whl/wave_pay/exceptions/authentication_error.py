from wave_pay.exceptions.flutterwave_error import FlutterWaveError


class AuthenticationError(FlutterWaveError):
    """
    Raised when the client library cannot authenticate with the gateway.  This generally means the public_key/private key are incorrect, or the user is not active.
    """
    pass
