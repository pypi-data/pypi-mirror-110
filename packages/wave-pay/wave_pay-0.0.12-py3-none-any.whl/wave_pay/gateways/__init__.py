from wave_pay.gateways.charges.card import Card
from wave_pay.gateways.charges.account import Bank
from wave_pay.gateways.charges.ussd import USSD
from wave_pay.gateways.charges.mpesa import MPESA
from wave_pay.gateways.transfers import TransferBase
from wave_pay.gateways.plans import Plan
from wave_pay.gateways.bills import BillPayment
from wave_pay.gateways.verification import Verification
from wave_pay.gateways.base.base import WaveBase


class Misc(WaveBase):

    def banks(self, country="NG"):
        return self.get("/banks/%s" % country)

    def settlements(self, params):
        return self.get("/settlements", params=params)

    def get_settlement(self, id_):
        return self.get("/settlements/%s" % id_)




