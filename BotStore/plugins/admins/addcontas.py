import os
import re
from asyncio.exceptions import TimeoutError
from datetime import datetime
from typing import Union

from pyrogram import Client, filters
from pyrogram.types import (
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardRemove,
)

from config import ADMINS
from database import cur, save
from utils import search_bin





async def iter_add_cards(cards):
    total = 0
    success = 0
    dup = []
    now = datetime.now()
    for row in re.finditer(
        r"(?P<tipo>\S+)[\|](?P<email>\S+)[\|](?P<senha>\S+)[\|](?P<cidade>\S+)",
        cards,
    ):
        total += 1
        #idcpf = row["cpf"][:6]
        #print(row["nome"])
        info = True
        is_valid = True
        s = int(20)
        sd = int(2025)
        if info:
            
            card = f'{row["email"]}'
            #if is_valid:
                #dup.append(f"{card} --- Vencida")
                #continue

            available = cur.execute(
                "SELECT added_date FROM contas WHERE email = ?", [row["email"]]
            ).fetchone()
            solds = cur.execute(
                "SELECT bought_date FROM contas_sold WHERE email = ?",
                [row["email"]],
            ).fetchone()
            dies = cur.execute(
                "SELECT added_date FROM contas WHERE email = ?",
                [row["email"]],
            ).fetchone()

            if available is not None:
                dup.append(f"{card} --- Repetida (adicionada em {available[0]})")
                continue

            if solds is not None:
                dup.append(f"{card} --- Repetida (vendida em {solds[0]})")
                continue

            if dies is not None:
                dup.append(f"""{card} --- Repetida ({row["email"]} ja esta no banco de dados)""")
                continue

            #level = info["level"].upper()

            # Alterações opcionais:
            # level = "NUBANK" if info["bank"].upper() == "NUBANK" else level

            #name = row["name"] if row["cpf"] else None

            cur.execute("INSERT INTO contas(tipo, email, senha, cidade) VALUES (?, ?, ?, ?)",
            (
            row["tipo"],
            row["email"],
            row["senha"],
            row["cidade"],
            ),
            )

            success += 1

    f = open("para_trocas.txt", "w")
    f.write("\n".join(dup))
    f.close()

    save()
    return (
        total,
        success,
    )


@Client.on_message(filters.regex(r"/betano( (?P<cards>.+))?", re.S) & filters.user(ADMINS))
async def on_add_m(c: Client, m: Message):
    cards = m.matches[0]["cards"]

    if cards:
        total, success = await iter_add_cards(cards)
        if not total:
            text = (
                "❌ Não encontrei Contas Betano na sua mensagem. Envie elas como texto ou arquivo."
            )
        else:
            text = f"✅ {success} Contas Betano adicionadas com sucesso. Repetidas/Inválidas: {(total - success)}"
        sent = await m.reply_text(text, quote=True)

        if open("para_trocas.txt").read() != "":
            await sent.reply_document(open("para_trocas.txt", "rb"), quote=True)
        os.remove("para_trocas.txt")

        return

    await m.reply_text(
        """💳 Modo de adição ativo. Envie as CONTAS PREMIUM como texto ou arquivo e elas serão adicionadas.
TIPO|EMAIL|SENHA|CIDADE (pode colocar qualquer cidade, na hora da compra isso não aparece)

EXEMPLO: /contas BETANO|email@gmail.com|senha|Sp""",
        reply_markup=ForceReply(),
    )

    first = True
    while True:
        if not first:
            await m.reply_text(
                "✅ Envie mais Contas Betano ou digite /done para sair do modo de adição.",
                reply_markup=ForceReply(),
            )

        try:
            msg = await c.wait_for_message(m.chat.id, timeout=300)
        except TimeoutError:
            kb = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton("❮ ❮", callback_data="start")]
                ]
            )

            await m.reply_text(
                "❕ Não recebi uma resposta para o comando anterior e ele foi automaticamente cancelado.",
                reply_markup=kb,
            )
            return

        first = False

        if not msg.text and (
            not msg.document or msg.document.file_size > 100 * 1024 * 1024
        ):  # 100MB
            await msg.reply_text(
                "❕ Eu esperava um texto ou documento contendo as LOGINS.", quote=True
            )
            continue
        if msg.text and msg.text.startswith("/done"):
            break

        if msg.document:
            cache = await msg.download()
            with open(cache) as f:
                msg.text = f.read()
            os.remove(cache)

        total, success = await iter_add_cards(msg.text)

        if not total:
            text = (
                "❌ Não encontrei Contas betano na sua mensagem. Envie elas como texto ou arquivo."
            )
        else:
            text = f"✅ {success} Contas Betano adicionadas com sucesso. Repetidas/Inválidas: {(total - success)}"
        sent = await msg.reply_text(text, quote=True)

        if open("para_trocas.txt").read() != "":
            await sent.reply_document(open("para_trocas.txt", "rb"), quote=True)
        os.remove("para_trocas.txt")

    await m.reply_text(
        "✅ Você Saiu do modo de adição de Contas Betano.", reply_markup=ReplyKeyboardRemove()
    )














