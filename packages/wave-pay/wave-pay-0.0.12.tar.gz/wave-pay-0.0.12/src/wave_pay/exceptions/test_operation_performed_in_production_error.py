from wave_pay.exceptions.flutterwave_error import FlutterWaveError


class TestOperationPerformedInProductionError(FlutterWaveError):
    """
    Raised when an operation that should be used for testing is used in a production environment
    """
    pass
