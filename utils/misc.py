from PIL import Image
import time
import random
import string
import yaml


class Misc:
    from utils.config import data

    @staticmethod
    async def create_growid():
        timestamp = int(time.time())
        random_string = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=6)
        )
        transaction_code = f"{timestamp}{random_string}"
        return transaction_code

    @staticmethod
    async def format_rupiah(nilai):
        return f"Rp {nilai:,.2f}".replace(".", ",").replace(",", ".", 1)

    @staticmethod
    async def calculate_rate_dl(rate_dl, amount):
        return round((amount / rate_dl) * 100)

    @staticmethod
    async def get_image_type(file_path):
        try:
            with Image.open(file_path) as img:
                return img.format
        except (IOError, AttributeError):
            return None

    @staticmethod
    async def split_array(arr, per_page):
        return [arr[i : i + per_page] for i in range(0, len(arr), per_page)]

    @staticmethod
    async def calculate_discount(harga_asli, harga_diskon):
        if harga_asli <= 0:
            raise ValueError("number is not valid")
        diskon_persen = ((harga_asli - harga_diskon) / harga_asli) * 60
        return round(diskon_persen)

    @staticmethod
    async def format_price(price):
        bgl = price // 10000
        remaining_after_bgl = price % 10000

        dl = remaining_after_bgl // 100
        wl = remaining_after_bgl % 100

        result = []

        if bgl > 0 or price >= 10000:
            result.append(f"{bgl} {Misc.data['emoji_blue_gem_lock']}")
            result.append(f"{dl} {Misc.data['emoji_diamond_lock']}")
            result.append(f"{wl} {Misc.data['emoji_world_lock']}")
        elif dl > 0:
            result.append(f"{dl} {Misc.data['emoji_diamond_lock']}")
            result.append(f"{wl} {Misc.data['emoji_world_lock']}")
        else:
            result.append(f"{wl} {Misc.data['emoji_world_lock']}")

        return " ".join(result)
