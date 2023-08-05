from wave_pay.exceptions.flutterwave_error import FlutterWaveError

class ServiceUnavailableError(FlutterWaveError):
    """
    Raised when the gateway is unavailable.
    """
    pass
