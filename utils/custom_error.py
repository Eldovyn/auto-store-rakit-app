from nextcord.ext import commands


class DataNotFound(commands.CheckFailure):
    def __init__(self, category, data):
        self.category = category
        self.data = data
        super().__init__(f"data not found {self.data}")


class DuplicateData(commands.CheckFailure):
    def __init__(self, category, data):
        self.category = category
        self.data = data
        super().__init__(f"duplicate data {self.data}")


class BalanceNotEnough(commands.CheckFailure):
    def __init__(self, category, amount):
        self.category = category
        self.amount = amount
        super().__init__(f"balance not enough {self.amount}")


class OnMaintenance(commands.CheckFailure):
    def __init__(self):
        super().__init__("bot is on maintenance")


class ImageNotAllow(commands.CheckFailure):
    def __init__(self, image_type):
        self.image_type = image_type
        super().__init__(f"{image_type} not allow")


class DiscountNotAllow(commands.CheckFailure):
    def __init__(self, price):
        self.price = price
        super().__init__(f"price not allow {self.price}")


class NumberNotAllow(commands.CheckFailure):
    def __init__(self, number):
        self.number = number
        super().__init__(f"number not allow {self.number}")


class ChannelNotAllow(commands.CheckFailure):
    def __init__(self, channel):
        self.channel = channel
        super().__init__(f"channel not allow at {self.channel}")


class TimeInvalid(commands.CheckFailure):
    def __init__(self, time):
        self.time = time
        super().__init__(f"time invalid {self.time}")


class DisableQris(commands.CheckFailure):
    def __init__(self):
        super().__init__("qris not available")


class InvalidModeLiveStock(Exception):
    def __init__(self):
        super().__init__("Invalid mode live stock")
