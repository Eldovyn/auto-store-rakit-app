from nextcord.ext import commands
import re
from .custom_error import TimeInvalid
from typing import Union
import nextcord


class TimeConverter(commands.Converter):
    async def convert(
        self, ctx: Union[commands.Context, nextcord.Interaction], argument: str
    ):
        args = argument.lower()
        satuan_waktu = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
        pola_waktu = re.compile(r"(\d+(?:\.\d+)?)([smhdw])")

        match = pola_waktu.fullmatch(args)
        if match:
            nilai, satuan = map(match.group, (1, 2))
            return float(nilai) * satuan_waktu[satuan]
        raise TimeInvalid(args)
