from wave_pay.exceptions.flutterwave_error import FlutterWaveError


class AuthorizationError(FlutterWaveError):
    """
    Raised when the user does not have permission to complete the requested operation.
    """
    pass
