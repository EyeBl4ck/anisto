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

@Client.on_callback_query(filters.regex(r"^comprar$"))
async def comprar(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("🖇 Enviar Comprovante 🖇", url="t.me/SuporteFenixLogins"),
                InlineKeyboardButton("❮ Voltar ❮", callback_data="esquemas"),
            ],
        ]
    )

    await m.edit_message_text(

        f"""<a href='https://i.ibb.co/dLhDybV/fenix-store.jpg'>&#8204</a>
<b>🛒 | Comprar Acesso manual !!!</b>

<b>💠 - :<CHAVE ALEATORIA> <code>7faf2802-c71b-4cd4-a8ea-13d02a5a5558</code></b>
<b>🔍 - Nome: <code>Ana Paula do rocio Marques</code></b>
<b>💰 - Valor: <code>R$: 20,00</code></b>

<b>⚠ OBS: Apos realizar o pagamento mande o comprovante para @SuporteFenixLogins.

</b>""",
  reply_markup=kb,
    )