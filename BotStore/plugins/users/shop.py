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
from utils import create_mention, get_info_wallet, dobrosaldo
from config import BOT_LINK
from config import BOT_LINK_SUPORTE


@Client.on_callback_query(filters.regex(r"^consull$"))
async def btc(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            
            
             [
                 InlineKeyboardButton("⬅️ Voltar", callback_data="start"),
             ],

        ]
    )
    await m.edit_message_text(
        f"""<b>🎁 Bônus de recarga: {dobrosaldo()}</b>""",
        reply_markup=kb,
    ) 
@Client.on_message(filters.command(["shop", "shop"]))
@Client.on_callback_query(filters.regex("^shop$"))
async def shop(c: Client, m: Union[Message, CallbackQuery]):
    user_id = m.from_user.id

    rt = cur.execute(
        "SELECT id, balance, balance_diamonds, refer FROM users WHERE id=?", [user_id]
    ).fetchone()

    if isinstance(m, Message):
        """refer = (
            int(m.command[1])
            if (len(m.command) == 2)
            and (m.command[1]).isdigit()
            and int(m.command[1]) != user_id
            else None
        )

        if rt[3] is None:
            if refer is not None:
                mention = create_mention(m.from_user, with_id=False)

                cur.execute("UPDATE users SET refer = ? WHERE id = ?", [refer, user_id])
                try:
                    await c.send_message(
                        refer,
                        text=f"<b>O usuário {mention} se tornou seu referenciado.</b>",
                    )
                except BadRequest:
                    pass"""

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
        
        [
                InlineKeyboardButton("📦 Trocar pontos", callback_data="swap"),
                InlineKeyboardButton("?duvidas?", url="t.me/polarbrabo"),
            ],
            [
                InlineKeyboardButton("⬅️ Voltar", callback_data="start"),
               
                
            ],
        ]
    )

    bot_logo, news_channel, support_user = cur.execute(
        "SELECT main_img, channel_user, support_user FROM bot_config WHERE ROWID = 0"
    ).fetchone()

    start_message = f"""‌<b>🛒 | Trocar pontos</b>

<b>Ao clica em trocar pontos seus pontos serão convertidos em saldo na store !</b>

<b>💸 Mínimo para poder trocar  10 (pontos)
💎 Seus pontos: 0
💰 Você irá receber 0 de saldo</b>"""

    if isinstance(m, CallbackQuery):
        send = m.edit_message_text
    else:
        send = m.reply_text
    save()
    await send(start_message, reply_markup=kb)
