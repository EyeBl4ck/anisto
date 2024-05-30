from typing import Union

from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from database import cur, save
from utils import create_mention, get_info_wallet

@Client.on_callback_query(filters.regex(r"^laras$"))
async def laras(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("📷 Enviar Comprovante 📷", url="t.me/SuporteFenixLogins"),
                InlineKeyboardButton("⏪ Voltar", callback_data="esquemas"),
            ],
        ]
    )

    await m.edit_message_text(
        f"""<a href='https://t.me/SuporteFenixLogins'>&#8204</a>
<b>🛒 | Comprar Lara, Pagamento por Chave Aleatoria !!!</b>

<b>💠 - <CHAVE EMAIL> <code>voltopolar@gmail.com</code></b>
<b>🔍 - Nome: <code>luiz henrique martins pereira</code></b>

<b>⚠ Apos realizar o pagamento mande o comprovante</b>
<b>⚠ OBS: Envie somente o Valor da Lara que você deseja comprar !</b>


</b>""",
  reply_markup=kb,
    )