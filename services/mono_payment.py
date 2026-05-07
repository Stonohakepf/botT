import requests
import uuid
from bot.config import MONO_TOKEN

MONO_URL = "https://api.monobank.ua/api/merchant/invoice/create"


def create_mono_invoice(amount: int, telegram_id: int):

    order_id = str(uuid.uuid4())

    headers = {
        "X-Token": MONO_TOKEN
    }

    payload = {
        "amount": amount * 100, 
        "ccy": 980,
        "merchantPaymInfo": {
            "reference": order_id,
            "destination": f"ISP payment {telegram_id}"
        },
        "redirectUrl": "https://t.me/RO_NET_bot",
        "webHookUrl": None 
    }

    r = requests.post(MONO_URL, json=payload, headers=headers)

    data = r.json()

    if "pageUrl" not in data:
        return {
            "ok": False,
            "error": data
        }

    return {
        "ok": True,
        "invoice_id": order_id,
        "pay_url": data["pageUrl"]
    }