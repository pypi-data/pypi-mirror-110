from wave_pay.exceptions.flutterwave_error import FlutterWaveError

class RequestTimeoutError(FlutterWaveError):
    """
    Raised when a client api timeout occurs.
    """
    pass
