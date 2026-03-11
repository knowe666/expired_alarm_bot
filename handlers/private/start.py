from aiogram import types
from aiogram.dispatcher.filters import Command
from handlers.chat_filters import IsPrivate, IsWallet
from loader import dp
from utils.script import check_domains, get_domains, check_on_address


@dp.message_handler(IsWallet())
async def add_wallet(message: types.Message):
    await message.answer('Ожидайте.')
    data_wallets = message.text.split()
    all_domains = []
    all_on_wallet = dict()
    for wallet in data_wallets:
        wallet = wallet.strip()
        all_domains.extend(get_domains(wallet))
        all_on_wallet.update(check_on_address(wallet))
    await message.answer(f"Обнаружено {len(all_domains)} доменов.\n"
                         f"Ожидайте примерно {round((len(all_domains)-len(all_on_wallet))/3)} сек.")
    result = check_domains(all_domains, all_on_wallet)
    text = '<code>'
    large_domain = min(max({len(i[2]) for i in result}), 22)
    for domain in result:
        days = str(domain[0].days)
        days = ' '*(3-len(days)) + days
        if len(data_wallets) > 1:
            add_text = f"{domain[2]}{' '*(large_domain-len(domain[2]))} {domain[4]} {days}d {domain[1].strftime('%d.%m')}{domain[3]}\n"
        else:
            add_text = f"{domain[2]}{' '*(large_domain-len(domain[2]))} {days}d {domain[1].strftime('%d.%m')}{domain[3]}\n"
        if len(text + add_text) > 4085:
            await message.answer(text + "</code>", parse_mode="html")
            text = '<code>' + add_text
        else:
            text += add_text
    await message.answer(text + "</code>", parse_mode="html")


@dp.message_handler(IsPrivate(), Command("start", prefixes="/"))  # TODO приватный фильтр убрать
async def start_command(message: types.Message):
    print(message)
    await message.answer("Привет!\n"
                         "Отправь мне один или несколько адресов кошельков в сети TON, а я пришлю все домены, которыми они владеют, с датой истечения.\n\n"
                         "Hello!\n"
                         "Send me one or more wallet addresses on the TON network, and I will send you all the domains they own, with the expiration date.")
