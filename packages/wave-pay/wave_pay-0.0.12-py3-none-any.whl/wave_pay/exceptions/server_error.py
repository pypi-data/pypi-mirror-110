from wave_pay.exceptions.flutterwave_error import FlutterWaveError


class ServerError(FlutterWaveError):
    """
    Raised when the gateway raises an error.  Please contant support at support@getpaystack.com.

    See https://developers.paystackpayments.com/reference/general/exceptions/python#server-error
    """
    pass
