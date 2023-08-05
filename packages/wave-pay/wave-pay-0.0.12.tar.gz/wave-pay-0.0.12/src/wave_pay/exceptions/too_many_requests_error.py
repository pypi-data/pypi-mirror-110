from wave_pay.exceptions.flutterwave_error import FlutterWaveError


class TooManyRequestsError(FlutterWaveError):
    """
    Raised when the rate limit api threshold is exceeded.
    """
    pass
