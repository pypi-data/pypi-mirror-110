from flutterwave_api.exceptions.flutterwave_error import FlutterWaveError

class ServiceUnavailableError(FlutterWaveError):
    """
    Raised when the gateway is unavailable.
    """
    pass
