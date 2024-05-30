import os
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


def is_valid(now: datetime, month: Union[str, int], year: Union[str, int]) -> bool:
    """Verifica se a CC está dentro da data de validade."""
    now_month = now.month
    now_year = now.year

    # Verifica se o ano for menor que o ano atual.
    if int(year) < now_year:
        return False

    # Se o ano for o mesmo que o atual, verifica se o mês é menor que o atual.
    if int(month) < now_month and now_year == int(year):
        return False

    return True


async def iter_add_cards_consul(cards):
    total = 0
    success = 0
    dup = []
    now = datetime.now()

    for row in cards.split("\n"):
        values = row.split("|")
        if len(values) != 10:
            dup.append(f"{row} --- Formato inválido")
            continue

        cc, mes, ano, cvv, nomebanco, _, _, _, limite, preco = values
        name = values[6].strip()  # Remove espaços em branco antes e depois do nome

        total += 1
        year = "20" + ano if ano.isdigit() and len(ano) == 2 else ano
        cvv = cvv if cvv else ""  # Trata o valor None como uma string vazia
        card = f'{cc}|{mes}|{year}|{cvv.zfill(3)}|{nomebanco}'  # Usa a variável 'year' em vez de 'row["ano"]'

        if not is_valid(now, mes, year):
            dup.append(f"{card} --- Data inválida (mes ou ano não estão presentes)")
            continue

        available = cur.execute(
            "SELECT added_date FROM consul WHERE cc = ?", [cc]
        ).fetchone()
        solds = cur.execute(
            "SELECT bought_date FROM cards_sold WHERE number = ?",
            [cc],
        ).fetchone()
        dies = cur.execute(
            "SELECT die_date FROM cards_dies WHERE number = ?",
            [cc],
        ).fetchone()

        if available is not None:
            dup.append(f"{card} --- Repetida (adicionada em {available[0]})")
            continue

        if solds is not None:
            dup.append(f"{card} --- Repetida (vendida em {solds[0]})")
            continue

        if dies is not None:
            dup.append(f"{card} --- Repetida (marcada como die em {dies[0]})")
            continue

        level = nomebanco.upper()

        cur.execute(
            "INSERT INTO consul(limite, preco, anjo, token, cc, bincc, senha, mes, ano, cvv, cpf, telefone, nome, added_date, nomebanco, pending) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                limite.strip(),  # Remove espaços em branco antes e depois do limite
                preco.strip(),   # Remove espaços em branco antes e depois do preco
                None,
                None,
                cc.strip(),  # Remove espaços em branco antes e depois do cc
                None,
                cvv,
                mes.strip(),  # Remove espaços em branco antes e depois do mes
                year.strip(),  # Remove espaços em branco antes e depois do ano
                cvv,
                None,
                None,
                name,
                now,
                level,
                0,
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


@Client.on_message(filters.command("con") & filters.user(ADMINS))
async def on_add_m(c: Client, m: Message):
    if len(m.command) > 1:
        cards = m.command[1]
        total, success = await iter_add_cards_consul(cards)

        if not total:
            text = (
                "❌ Não encontrei Consuls na sua mensagem. Envie elas como texto ou arquivo."
            )
        else:
            text = f"✅ {success} Consuls adicionadas com sucesso. Repetidas/Inválidas: {(total - success)}"
        sent = await m.reply_text(text, quote=True)

        if open("para_trocas.txt").read() != "":
            await sent.reply_document(open("para_trocas.txt", "rb"), quote=True)
        os.remove("para_trocas.txt")

        return

    await m.reply_text(
        "💳 Modo de adição ativo. Envie as Consuls como texto ou arquivo e elas serão adicionadas.",
        reply_markup=ForceReply(),
    )

    first = True
    while True:
        if not first:
            await m.reply_text(
                "✅ Envie mais CCs ou digite /done para sair do modo de adição.",
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
                "❕ Eu esperava um texto ou documento contendo as CCs.", quote=True
            )
            continue
        if msg.text and msg.text.startswith("/done"):
            break

        if msg.document:
            cache = await msg.download()
            with open(cache) as f:
                msg.text = f.read()
            os.remove(cache)

        total, success = await iter_add_cards_consul(msg.text)

        if not total:
            text = (
                "❌ Não encontrei Consul na sua mensagem. Envie elas como texto ou arquivo."
            )
        else:
            text = f"✅ {success} Consul adicionadas com sucesso. Repetidas/Inválidas: {(total - success)}"
        sent = await msg.reply_text(text, quote=True)

        if open("para_trocas.txt").read() != "":
            await sent.reply_document(open("para_trocas.txt", "rb"), quote=True)
        os.remove("para_trocas.txt")

    await m.reply_text(
        "✅ Você Saiu do modo de adição de CCs.", reply_markup=ReplyKeyboardRemove()
    )
