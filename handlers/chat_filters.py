from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
alf_wallet = set("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-_0123456789")


class IsGroup(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type in (types.ChatType.GROUP, types.ChatType.SUPERGROUP)


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


class IsWallet(BoundFilter):
    async def check(self, message: types.Message):
        data_list = message.text.split()
        for wallet in data_list:
            message_text = wallet.strip()
            if len(message_text) != 48:
                return False
            for i in message_text:
                if i not in alf_wallet:
                    return False
        return True
