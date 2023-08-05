from flutterwave_api.gateways.charges.card import Card
from flutterwave_api.gateways.charges.account import Bank
from flutterwave_api.gateways.charges.ussd import USSD
from flutterwave_api.gateways.charges.mpesa import MPESA
from flutterwave_api.gateways.transfers import TransferBase
from flutterwave_api.gateways.plans import Plan
from flutterwave_api.gateways.bills import BillPayment
from flutterwave_api.gateways.verification import Verification
from flutterwave_api.gateways.base.base import WaveBase


class Misc(WaveBase):

    def banks(self, country="NG"):
        return self.get("/banks/%s" % country)

    def settlements(self, params):
        return self.get("/settlements", params=params)

    def get_settlement(self, id_):
        return self.get("/settlements/%s" % id_)




