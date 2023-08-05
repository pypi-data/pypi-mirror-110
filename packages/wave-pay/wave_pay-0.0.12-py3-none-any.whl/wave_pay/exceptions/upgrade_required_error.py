from wave_pay.exceptions.flutterwave_error import FlutterWaveError


class UpgradeRequiredError(FlutterWaveError):
    """
    Raised for unsupported client library versions.
    """
    pass
