import yaml
import time
import random
import string
import midtransclient
import datetime


class QrisPayment:
    from utils.config import data as data_content

    def __init__(self):
        self.api = midtransclient.CoreApi(
            is_production=True,
            server_key=self.data_content["server_key"],
            client_key=self.data_content["client_key"],
        )

    async def parse_rupiah(self, formatted):
        nilai_str = formatted.replace("Rp ", "")
        nilai_str = nilai_str.replace(",", "").replace(".", "")
        nilai_str = nilai_str[:-2] + "." + nilai_str[-2:]
        nilai = float(nilai_str)
        if nilai.is_integer():
            nilai = int(nilai)
        return nilai

    async def create_code(self):
        timestamp = int(time.time())
        random_string = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        transaction_code = f"TX{timestamp}{random_string}"
        return transaction_code

    async def check_status(self, unique_code):
        try:
            transaction_status = self.api.transactions.status(unique_code)
            return transaction_status
        except Exception as e:
            return e

    async def cancel_qris(self, unique_code):
        try:
            cancel_response = self.api.transactions.cancel(unique_code)
            return cancel_response
        except Exception as e:
            return e

    async def create_qris(self, unique_code, amount):
        order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S +0700")
        params = {
            "payment_type": "gopay",
            "transaction_details": {
                "order_id": unique_code,
                "gross_amount": amount,
            },
            "custom_expiry": {
                "order_time": order_time,
                "expiry_duration": 5,
                "unit": "minute",
            },
        }
        transaction = self.api.charge(params)
        return transaction
