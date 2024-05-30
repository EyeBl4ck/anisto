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


@Client.on_message(filters.command(["ferramenta", "ferramentas"]))
@Client.on_callback_query(filters.regex("^ferramenta$"))
async def ferramentas(c: Client, m: Union[Message, CallbackQuery]):
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
                InlineKeyboardButton(text="✅ Concordar", callback_data="start"),
            ],
        ]
    )

    bot_logo, news_channel, support_user = cur.execute(
        "SELECT main_img, channel_user, support_user FROM bot_config WHERE ROWID = 0"
    ).fetchone()

    start_message = f"""‌<b>1️⃣ -  Crie um cadastro na Americanas, Submarino ou Magazine Luiza </b>

<b>2️⃣ - Selecione um produto que com frete totalize até R$50, ou coloque para retirar no local</b>

<b>3️⃣ - Essa é a parte mais importante para sua troca ser realizada com sucesso, você devera comprar o produto com a CC adquirida na nossa Base, esse momento deve ser GRAVADO e enviado no nosso chat JUNTO da mensagem que o bot entregou a CC
(SE ESSE PASSO A PASSO NAO FOR SEGUIDO, VOCE NAO RECEBERA SUA TROCA)</b>

<b>4️⃣ - Após o vídeo ser enviado nossa equipe ira analisar ele, se foi gravado no prazo de 20 MINUTOS e se a CC inserida foi digitada corretamente</b>

<b>5️⃣ - Com tudo certo o suporte ira lhe enviar o gift, que basta você copiar a mensagem que esta no formato a seguir de exemplo: /resgatar MGLL8MSUBWIW e envia-la  no chat do bot @FenixLoginsBot</b>

<code>⚠️ TROCAS SOMENTE DE CC DIE
❌ NÃO GARANTO SALDO

⚠️ Evite testar em conta Americanas com vários pedidos cancelados ou com seu ip sujo, tenha preferencia por 4g, caso contrario tera grandes chances de negar a CC instantaneamente e você achar que ela esta DIE</code>

<b>🕗Prazos de 25 Minutos para UNITARIAS adquiridas no Bot</b>

<b>Tudo isso é feito para você ter uma troca JUSTA, com um atendimento humano e evitando que você perca dinheiro, caso contrário a troca não será realizada e caso haja insistência você será Banido.</b>"""

    if isinstance(m, CallbackQuery):
        send = m.edit_message_text
    else:
        send = m.reply_text
    save()
    await send(start_message, reply_markup=kb)
