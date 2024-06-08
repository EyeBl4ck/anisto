import asyncio

from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from config import ADMIN_CHAT
from config import GRUPO_PUB
from config import BOT_LINK
from config import BOT_LINK_SUPORTE
from database import cur, save
from utils import (
    create_mention,
    get_info_wallet,
    get_price,
    insert_docs_sold,
    insert_sold_balance,
    lock_user_buy,
    msg_buy_off_user,
    msg_buy_user,
    msg_group_adm,
    msg_group_publico,
)



SELLERS, TESTED = 0, 0


T = 0.1





# Listagem de tipos de compra.
@Client.on_callback_query(filters.regex(r"^comprar_doc$"))
async def comprar_doc_list(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("🛒 DOC", callback_data="comprar_doc unit"),
                
                
            ],
          

             
            [
                InlineKeyboardButton("🔙 Voltar", callback_data="start"),
            ],
        ]
    )

    await m.edit_message_text(
        f"""<b>📂 | !!! Página de Compras !!!</b>
<b>a melhor plataforma brasileira para compra de doc, logins, burladores, e consul.</b>

{get_info_wallet(m.from_user.id)}""",
        reply_markup=kb,
    )


# Pesquisa de CCs via inline.
@Client.on_inline_query(filters.regex(r"^buscar_(?P<type>\w+) (?P<value>.+)"))
async def search_cc(c: Client, m: InlineQuery):
    """
    Pesquisa uma documentos via inline por tipo e retorna os resultados via inline.

    O parâmetro `type` será o tipo de valor para pesquisar
    """

    typ = m.matches[0]["type"]
    qry = m.matches[0]["value"]

    # Não aceitar outros valores para prevenir SQL Injection.
    if typ not in ("doc", "docs", "score", "cidade"):
        return

    if typ != "bicos":
        qry = f"%{qry}%"

    if typ == "doc":
        typ2 = "level"
        typ3 = "nome"
    elif typ == "cidade":
        typ2 = "level"
        typ3 = "localidade"
    elif typ == "score":
        typ2 = "level"
        typ3 = "score"
    else:
        typ2 = typ

    rt = cur.execute(
        f"SELECT cpf, nome,  {typ2}, idcpf, score, localidade FROM docscnh WHERE {typ3} LIKE ? AND pending = 0 ORDER BY RANDOM() LIMIT 40",
        [qry.upper()],
    ).fetchall()

    results = []
    results.append(
            InlineQueryResultArticle(
                title=f"Total: ({len(rt)}) de resultados encontrados",
                description="Confira todos os doc abaixo 🛍👇",
                
                input_message_content=InputTextMessageContent(
                    "Compre documentos via Inline ✅"
                ),
            )
        )

    wallet_info = get_info_wallet(m.from_user.id)

    for cpf, nome, value, idcpf, score, localidade in rt:

        price = await get_price("docs", value)

        base = f"""Nome: {nome}"""

        base_ml = f"""<b>Nome:</b> <i>{nome}</i>
<b>Tipo:</b> <i>{value}</i>
<b>Valor:</b> <i>R$ {price}</i>"""

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Comprar",
                        callback_data=f"buy_off idcpf '{idcpf}' {value}",
                    )
                ]
            ]
        )

        results.append(
            InlineQueryResultArticle(
                title=f"{typ} {value} - R$ {price}",
                description=base,
                
                input_message_content=InputTextMessageContent(
                    base_ml + "\n\n" + wallet_info
                ),
                reply_markup=kb,
            )
        )

    await m.answer(results, cache_time=5, is_personal=True)
    

# Opção Compra de CCs e Listagem de Level's.
@Client.on_callback_query(filters.regex(r"^comprar_doc unit$"))
async def comprar_ccs(c: Client, m: CallbackQuery):
    list_levels_cards = cur.execute("SELECT level FROM docscnh GROUP BY level").fetchall()
    levels_list = [x[0] for x in list_levels_cards]

    if not levels_list:
        return await m.answer(
            "⚠️ Não há métodos disponíveis no momento, tente novamente mais tarde.",
            show_alert=True,
        )

    levels = []
    for level in levels_list:
        level_name = level
        n = level.split()
        if len(n) > 1:
            level_name = n[0][:4] + " " + n[1]

        price = await get_price("docs", level)
        levels.append(
            InlineKeyboardButton(
                text=f"{level_name.upper()} | R$ {price} - Aleatório 🎲",
                callback_data=f"buy_offs level '{level}'",
            )
        )

    organ = (
        lambda data, step: [data[x : x + step] for x in range(0, len(data), step)]
    )(levels, 2)
    table_name = "docscnh"
    ccs = cur.execute(
        f"SELECT level, count() FROM {table_name} GROUP BY level ORDER BY count() DESC"
    ).fetchall()

    
    total = f"\n<b>📂 | Total de doc</b>: {sum([int(x[1]) for x in ccs])}" if ccs else ""
    organ.append([InlineKeyboardButton(
                    "🛒 Buscar doc por Nome",
                    switch_inline_query_current_chat="buscar_doc A",
                )])
    organ.append([InlineKeyboardButton(text="🔙 Voltar", callback_data="comprar_doc")])
    kb = InlineKeyboardMarkup(inline_keyboard=organ)
    await m.edit_message_text(
        f"""<b>🛍 Lista de doc unitário, 
        
<b>⚠️ Escolha o doc conforme os botões inline abaixo e seja feliz usando nossos produtos</b>
{total}

{get_info_wallet(m.from_user.id)}""",
        reply_markup=kb,
    )




@Client.on_callback_query(
    filters.regex(r"^buy_off (?P<type>[a-z]+) '(?P<level_cc>.+)' ?(?P<other_params>.+)?")  # fmt: skip
)
@lock_user_buy
async def buy_off(c: Client, m: CallbackQuery):
    user_id = m.from_user.id
    balance: int = cur.execute("SELECT balance FROM users WHERE id = ?", [user_id]).fetchone()[0]  # fmt: skip
    type_cc = m.matches[0]["type"]
    level_cc = m.matches[0]["level_cc"]
    tipo = m.matches[0]["other_params"]

    price = await get_price("docs", tipo)

    if balance < price:
        return await m.answer(
            "⚠️ Você não possui saldo suficiente para esse item. Por favor, faça uma transferência usando /pix",
            show_alert=True,
        )

    search_for = "level" if type_cc == "level" else "idcpf"

    selected_cc = cur.execute(
        f"SELECT nome, cpf, linkdoc, added_date, level, idcpf, score, localidade FROM docscnh WHERE {search_for} = ? AND pending = ? ORDER BY RANDOM()",
        [level_cc, False],
    ).fetchone()

    if not selected_cc:
        return await m.answer("⚠️ Sem doc disponiveis para este nivel.", show_alert=True)

    diamonds = round(((price / 100) * 8), 2)
    new_balance = balance - price
    
    (
        nome,
        cpf,
        linkdoc,
        added_date,
        tipo,
        idcpf,
        score,
        localidade,
    ) = selected_cc
    #nome = nome.upper()
    card = "|".join([nome, cpf, linkdoc])
    ds = "docs"
    list_card_sold = selected_cc + (user_id, ds)

    cur.execute(
        "DELETE FROM docscnh WHERE cpf = ?",
        [selected_cc[1]],
    )

    cur.execute(
        "UPDATE users SET balance = ?, balance_diamonds = round(balance_diamonds + ?, 2) WHERE id = ?",
        [new_balance, diamonds, user_id],
    )

    s = insert_docs_sold(list_card_sold)
    print(s)
    insert_sold_balance(price, user_id, "docs")

    #dados = (cpf, name) if cpf is not None else None
    base = await msg_buy_off_user(user_id, nome, cpf, tipo, price, linkdoc)
    await m.edit_message_text(base)
    mention = create_mention(m.from_user)
    adm_msg = msg_group_adm(
        mention, nome, cpf, linkdoc, price, localidade, new_balance, score, tipo
    )
    await c.send_message(ADMIN_CHAT, adm_msg)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 Voltar", callback_data="comprar_doc"),
            ],
        ]
    )
    try:
        await m.message.reply_text(
            "✅ Compra realizada com sucesso. Clique no botão abaixo para voltar para o menu principal.",
            reply_markup=kb,
        )
    except:
        ...
    save()
    
    
    
@Client.on_callback_query(
    filters.regex(r"^buy_offs (?P<type>[a-z]+) '(?P<level_cc>.+)' ?(?P<other_params>.+)?")  # fmt: skip
)
@lock_user_buy
async def buy_offs(c: Client, m: CallbackQuery):
    user_id = m.from_user.id
    balance: int = cur.execute("SELECT balance FROM users WHERE id = ?", [user_id]).fetchone()[0]  # fmt: skip

    type_cc = m.matches[0]["type"]
    level_cc = m.matches[0]["level_cc"]

    price = await get_price("docs", level_cc)

    if balance < price:
        return await m.answer(
            "⚠️ Você não possui saldo suficiente para esse item. Por favor, faça uma transferênci usando /pix.",
            show_alert=True,
        )

    search_for = "level" if type_cc == "level" else "idcpf"

    selected_cc = cur.execute(
        f"SELECT nome, cpf, linkdoc, added_date, level, idcpf, score, localidade FROM docscnh WHERE {search_for} = ? AND pending = ? ORDER BY RANDOM()",
        [level_cc, False],
    ).fetchone()

    if not selected_cc:
        return await m.answer("⚠️ Sem doc disponiveis para este nivel.", show_alert=True)

    diamonds = round(((price / 100) * 8), 2)
    new_balance = balance - price
    
    (
        nome,
        cpf,
        linkdoc,
        added_date,
        tipo,
        idcpf,
        score,
        localidade,
    ) = selected_cc
    #nome = nome.upper()
    card = "|".join([nome, cpf, linkdoc])
    ds = "docs"
    list_card_sold = selected_cc + (user_id, ds)

    cur.execute(
        "DELETE FROM docscnh WHERE cpf = ?",
        [selected_cc[1]],
    )

    cur.execute(
        "UPDATE users SET balance = ?, balance_diamonds = round(balance_diamonds + ?, 2) WHERE id = ?",
        [new_balance, diamonds, user_id],
    )

    s = insert_docs_sold(list_card_sold)
    print(s)
    insert_sold_balance(price, user_id, "docs")

    #dados = (cpf, name) if cpf is not None else None
    base = await msg_buy_off_user(user_id, nome, cpf, tipo, price, linkdoc)
    await m.edit_message_text(base)
    mention = create_mention(m.from_user)
    adm_msg = msg_group_adm(
        mention, nome, cpf, linkdoc, price, localidade, new_balance, score, tipo
    )
    await c.send_message(ADMIN_CHAT, adm_msg)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 Voltar", callback_data="comprar_doc"),
            ],
        ]
    )
    try:
        await m.message.reply_text(
            "✅ Compra realizada com sucesso. Clique no botão abaixo para voltar para o menu principal.",
            reply_markup=kb,
        )
    except:
        ...
    save()    
