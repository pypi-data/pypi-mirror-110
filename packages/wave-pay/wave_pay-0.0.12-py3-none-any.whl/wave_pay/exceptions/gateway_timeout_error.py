from wave_pay.exceptions.flutterwave_error import FlutterWaveError

class GatewayTimeoutError(FlutterWaveError):
    """
    Raised when a gateway response timeout occurs.
    """
    pass
