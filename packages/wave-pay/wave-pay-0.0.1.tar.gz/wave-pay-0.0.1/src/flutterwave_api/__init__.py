from flutterwave_api.configuration import Configuration
from flutterwave_api.utils.version import get_version, get_short_version

from flutterwave_api.gateways import (
    Bank,
    BillPayment,
    Card,
    Misc,
    MPESA,
    Plan,
    TransferBase,
    USSD,
    Verification
)


class WaveGateway:

    version = get_version()
    short_version = get_short_version()

    def __init__(self, secret_key, public_key, **kwargs):
        self.config = Configuration(secret_key=secret_key, public_key=public_key, **kwargs)
        self.Bank = Bank(self)
        self.Card = Card(self)
        self.USSD = USSD(self)
        self.Mpesa = MPESA(self)
        self.Transfer = TransferBase(self)
        self.Plan = Plan(self)
        self.Bills = BillPayment(self)
        self.Misc = Misc(self)
        self.Verification = Verification(self)
