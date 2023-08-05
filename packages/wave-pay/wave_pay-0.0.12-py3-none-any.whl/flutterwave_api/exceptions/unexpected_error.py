from flutterwave_api.exceptions.flutterwave_error import FlutterWaveError


class UnexpectedError(FlutterWaveError):
    """ Raised for unknown or unexpected errors. """
    pass
