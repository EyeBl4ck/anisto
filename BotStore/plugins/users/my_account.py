from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from database import cur, save
from utils import get_info_wallet



@Client.on_callback_query(filters.regex(r"^user_info$"))
async def user_info(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("⬅️ Voltar", callback_data="start"),
            ],
        ]
    )
    link = f"https://t.me/{c.me.username}?start={m.from_user.id}"
    await m.edit_message_text(
        f"""<b>ℹ️ Seus dados abaixo</b>

<b>👤 Username: {m.from_user.first_name}</b>
<b>🆔 Id: {m.from_user.id}</b>
<b>💠 Pix automatico: ativo</b>
<b>⚙️ Manutenção: desligado</b>

<b>⚠️ Como funciona?</b>
    
<b>1⃣ - Cada pessoa que for indicada pelo seu link e recarregar qualquer valor, você vai ganhar 10% do valor que ele recarregou, isso inclui todas as recargas que ele fizer!</b>

<b>2⃣ - Os valores serão concedidos automaticamente em dinheiro na sua conta cadastrada no bot! </b>

<b>3⃣- Quanto mais pessoas você indicar, mais você vai ganhar!</b>

<b>🎁 - Seu link de afiliação:</b>
<code>{link}</code></b>""",
        reply_markup=kb,
    )
    
@Client.on_callback_query(filters.regex(r"^gift$"))
async def gift(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            
            
             [
                 InlineKeyboardButton("⬅️ Voltar", callback_data="start"),
             ],

        ]
    )
    link = f""
    await m.edit_message_text(
        f"""<b>🎁 Resgatar Gift</b>
<i>- Aqui você resgatar o gift com facilidade,digite seu gift como o exemplo abaixo.</i>

<i>🏷 - Exemplo: /resgatar FOX0FCOT7OTH </i>

{get_info_wallet(m.from_user.id)}""",
        reply_markup=kb,
    )
@Client.on_callback_query(filters.regex(r"dv$"))
async def dv(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            
            
             [
                 InlineKeyboardButton("⬅️ Voltar", callback_data="user_info"),
             ],

        ]
    )

    await m.edit_message_text(
        f"""<b>💻 Software:</b>

<b> agradecimento - </b>
<b>É com grande entusiasmo que compartilhamos com vocês que estamos nos dedicando ao desenvolvimento de nossa loja para proporcionar a melhor experiência de compra possível. Apesar de ainda estarmos em fase de desenvolvimento, gostaríamos de compartilhar com vocês alguns detalhes sobre o que está por vir.</b>

<b>Nosso objetivo é criar uma loja online que seja uma referência em qualidade, diversidade de produtos e atendimento excepcional. Estamos trabalhando arduamente para garantir que cada detalhe seja cuidadosamente planejado e executado, a fim de proporcionar uma experiência de compra inigualável.</b>

<b>Nossa equipe está empenhada em selecionar os melhores produtos para você, desde itens de vestuário e acessórios, até eletrônicos, itens para a casa e muito mais. Queremos ser sua loja favorita, onde você poderá encontrar tudo o que precisa em um só lugar, sempre com produtos de alta qualidade e preços competitivos.</b>

<b>Estamos também investindo em uma plataforma de fácil navegação, para que você encontre o que procura de maneira rápida e intuitiva. Além disso, estamos trabalhando para garantir que as informações sobre os produtos sejam claras e detalhadas, para que você tenha total confiança em suas escolhas.</b>

<b>Acreditamos que o atendimento é fundamental para o sucesso de uma loja, por isso, estamos treinando nossa equipe para oferecer o melhor suporte ao cliente possível. Queremos resolver todas as suas dúvidas e problemas de forma ágil e eficiente, garantindo que você se sinta valorizado e assistido em todas as etapas.</b>

<b>Embora ainda estejamos em fase de desenvolvimento, queremos assegurar a vocês que estamos trabalhando incansavelmente para oferecer uma experiência de compra online de excelência. Agradecemos sua paciência e apoio ao longo desse processo, e pedimos que nos acompanhem em nossa jornada de crescimento.</b>

<b>Estejam certos de que em breve teremos o prazer de apresentar nossa loja totalmente desenvolvida, pronta para atender todas as suas necessidades. Com produtos de qualidade, fácil navegação e atendimento de excelência, queremos nos tornar sua loja de preferência.</b>

<b>Fiquem atentos às nossas redes sociais e futuras comunicações, para ficarem por dentro de todas as atualizações e lançamentos. Estamos entusiasmados com o futuro da nossa loja e estamos ansiosos para compartilhar essa jornada com todos vocês.</b>

<b> Agradecemos a compreensão e apoio de todos os clientes ativos em nossas lojas</b>

<b>👤 dev: @VigilMT</b>
<b>🤖 Versão da Store: 18.1</b>
<b>⚙ Atualizações: Fiz Varias Atualizações e arrumei bugs que tinham no Bot.</b>""",
  reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"regras$"))
async def regras(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("❮ ❮", callback_data="start"),
            ],
             [
                 InlineKeyboardButton("⚙ SUPORTE", url="https://t.me/venompcx"),
             ],
        ]
    )

    await m.edit_message_text(
        f"""<b> ❗❗❗ Regras Voltadas Para a Nossa Store de Contas Premium ❗❗❗ </b>

<code>Aqui estão as regras e trocas da nossa store de Contas Premium:
    
    1. Condições para troca da Conta:
    - Conta sem assinatura.
    - Conta com senha errada.
    - Conta que esta vencida.
   
    ❗ Para mais informações ou dúvidas, Chame o suporte.
</code>""",
  reply_markup=kb,
    )


@Client.on_callback_query(filters.regex(r"esquemas$"))
async def esquemas(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            
            [
                 InlineKeyboardButton("🛒 Comprar Acesso 🛒", callback_data="comprar"),
             ],
            [
                InlineKeyboardButton("❮ Voltar ❮", callback_data="start"),
            ],
        ]
    )

    await m.edit_message_text(
        f"""<b>🔥TEMOS UM CANAL DE METODOS E ESQUEMAS PRIVADO QUE TE ENSINAMOS TUDO DO BASICO AO AVANÇADO. TEMOS +5MIL TRAMPOS EM NOSSO CANAL! 

 | ACESSO VILICIO ( Pagar so 1 vez )
 | TRAMPOS POSTADOS DIARIAMENTE !
 | CANAL DE DONATES DE CC'S E BINS.
| 100% DE SUPORTE EM TODODOS OS TRAMPOS.
✍️ | TRAMPOS QUE DA PRA FAZER EM CELULAR E PC !
📖 | VARIOS CURSOS E ESQUEMAS EM PDF, TEXTO E VIDEO !

👁‍🗨𝘝𝘌𝘑𝘈 𝘜𝘔 𝘚𝘗𝘖𝘐𝘓𝘌𝘙 𝘋𝘖 𝘘𝘜𝘌 𝘛𝘌𝘔 𝘌𝘔 𝘕𝘖𝘚𝘚𝘖 𝘊𝘈𝘕𝘈𝘓⤵️

𝗧𝗨𝗧𝗨𝗥𝗜𝗔𝗦 𝗣𝗔𝗥𝗔 𝗙𝗔𝗭𝗘𝗥 𝗖𝗢𝗡𝗧𝗔𝗦 𝗦𝗧𝗥𝗘𝗔𝗠𝗜𝗡𝗚 
▪️Metodo Tidal
▪️Metodo Paramout+
▪️Metodo Prime video
▪️Metodo Netflix 2023
▪️Metodo Crunchyroll
▪️Metodo Twitch
▪️Metodo Spotify
▪️Metodo Hbo Max
▪️Metodo Scribd
▪️Metodo Duolingo
▪️Metodo Youtuber Premium
E vários outros metodos no canal...
-
🩹 𝗠𝗘𝗧𝗢𝗗𝗢𝗦 𝗘 𝗘𝗦𝗤𝗨𝗘𝗠𝗔𝗦 
▪️Metodo Seguidores na GG
▪️Esquema cria conta Motorista na Uber
▪️Metodo Recarga TIM
▪️Esquema fazendo Emprestimo ( Video )
▪️Metodo Ativando Plano da VIVO
▪️Esquema Lavando Dinheiro
▪️Metodo Reembolso Amazon
▪️Metodo Limpando Nome
▪️Esquema Lara Pj santander
▪️Metodo Volta Limite Nubank
▪️Esquema Colher Consultavel
▪️Metodo Para desbanir conta Telegram
▪️Esquema Colher Kit Bico
▪️Metodo Telegram Premium por 1 real
▪️Esquema Dropshipping
▪️Esquema Invadindo cameras de Lojas
▪️Metodo Desbanir Conta Telegram
▪️Esquema Golpe do iPhone
▪️Metodos de Laras sem DOCs
▪️Esquema Saque FGTS 2023
▪️Metodo Uber Cash 2023
▪️Esquema Whisky
▪️Metodo Ifood na GG 2023
▪️Esquema Uber na GG
▪️Metodo Lara sem DOC
▪️Esquema Voltando Limite de qualque card
E vários outros trampos no canal...
-
📚𝗖𝗨𝗥𝗦𝗢𝗦 𝗣𝗔𝗥𝗔 𝗚𝗔𝗡𝗛𝗔 𝗗𝗜𝗡𝗛𝗘𝗜𝗥𝗢 𝗡𝗢 𝟳
▪️Como Cria Laras do zero ( Video )
▪️Criando Bot em Php ( Video )
▪️Como Cria Banners/Artes/Logos ( Video )
▪️Como Cria Editaveis ( Video )
▪️Como Cria Bot de internet Vpn ( Video )
▪️Como Hospedar bot de CC + Source ( Video )
▪️Criando Pagina fake para colher CC/CONSUL ( Video )
▪️Script de Adicionar Membros em Grupos ( Video )
▪️Bot de Divulgaçao de Whatsapp ( Video )
▪️Curso de criaçao de notas Fakes
▪️+30 Paineis de Seguidores super barato 
▪️+20 Salas de Sinais de Casas de apostas 
▪️Packs de Editavel
E vários outros tuturiais no canal...
-
💰 𝗘𝗦𝗤𝗨𝗘𝗠𝗔𝗦 𝗣𝗥𝗔 𝗩𝗜𝗥𝗔 𝗦𝗔𝗟𝗗𝗢 🤑
▪️Virando saldo na Recargapay 2023
▪️Virando saldo com Boleto
▪️Virando saldo na MP 2023
▪️Virando saldo na Blaze
▪️Virando saldo na Paypal
▪️Virando saldo na Hotmart
▪️Virando saldo na Uber com GG
▪️Virando saldo na Perfectpay com GG
▪️Virando saldo na Stone
▪️Virando saldo na ITI
▪️Virando saldo na Picpay
▪️Virando saldo na Bagy
▪️Virando saldo na Sumup
▪️Virando saldo na Kiwify 2023
▪️Virando saldo na Eduzz
▪️Virando saldo na Enjoei
E vários outros esquemas no canal....
-
💳 𝗔𝗣𝗥𝗢𝗩𝗔𝗖‌𝗔𝗢 𝗘 𝗣𝗩𝗖𝘀 💳
▪️Aprovando Vinhos
▪️Esquema PVC Paraná
▪️Aprovando Jogos de Xbox na CC
▪️Esquema PVC Bari
▪️Aprovando PagSeguro
▪️Esquema PVC Nubank 2023
▪️Aprovando Perfume importados
▪️Esquema PVC Banco do Brasil
▪️Aprovando Bebidas/Comidas
▪️Esquema PVC Casas Bahia
▪️Aprovando amazon ( Conta Nova )
▪️Esquema PVC Porto Seguro
▪️Varias dicas de Aprovaçao
▪️Esquema PVC Itau
▪️Esquema PVC Bradesco
▪️Esquema PVC Atacadão
▪️+100 Sites aprovando com GG e CC
E vários outros trampos no canal...
-
• OS TRAMPOS ESTAO EM UM CANAL PRIVADO ENTRANDO NELE VOÇE VAI TE ACESSO A TODOS OS CONTEUDOS CITADO ACIMA E MUITOS MAIS!

• MUITOS ESQUEMAS FÁCEIS DE FAZER, SÃO + DE 5MIL METODOS E ESQUEMAS! PARA VOCE APRENDER DO ZERO AO PROFICIONAL, UTILIZANDO APENAS O SEU CELULAR OU PC.


↘️ 𝐂𝐎𝐌𝐏𝐑𝐄 𝐒𝐄𝐔 𝐀𝐂𝐄𝐒𝐒𝐎 𝐀𝐐𝐔𝐈 ↙️</b>""",
  reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"lara$"))
async def lara(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            
            [
                 InlineKeyboardButton("🛒 Comprar Lara 🛒", callback_data="laras"),
             ],
            [
                InlineKeyboardButton("⏪ Voltar", callback_data="start"),
            ],
        ]
    )

    await m.edit_message_text(
        f"""<b>😈🔥𝐀𝐌𝐄 𝐃𝐈𝐆𝐈𝐓𝐀𝐋 120,00
😈🔥𝐌𝐄𝐑𝐂𝐀𝐃𝐎 𝐏𝐀𝐆𝐎 140,00
😈🔥𝐕𝐈𝐕𝐎 𝐏𝐀𝐘 120,00
😈🔥𝐄𝐖𝐀𝐋𝐋𝐘 120,00
😈🔥𝐃𝐈𝐌𝐎 120,00
😈🔥𝐍𝐆 𝐂𝐀𝐒𝐇 120,00
😈🔥𝐎𝐍𝐁𝐀𝐍𝐊 120,00
😈🔥𝐒𝐔𝐏𝐄𝐑 𝐃𝐈𝐆𝐈𝐓𝐀𝐋 120,00
😈🔥𝐁𝐈𝐏𝐀 120,00
😈🔥𝐂𝐀𝐏𝐈𝐓𝐔𝐀𝐋 140,00
😈🔥𝐑𝐄𝐃𝐄 𝐂𝐄𝐋𝐂𝐎𝐈𝐍 100,00
😈🔥𝐕𝐎𝐋𝐓𝐙 120,00
😈🔥𝐌𝐄𝐋𝐈𝐔𝐙 120,00
😈🔥𝐑𝐄𝐂𝐀𝐑𝐆𝐀𝐏𝐀𝐘 175,00
😈🔥𝐒𝐀𝐍𝐓𝐀𝐍𝐃𝐄𝐑 𝐂𝐍𝐏𝐉 500,00
😈🔥𝐌𝐄𝐑𝐂𝐀𝐃𝐎 𝐏𝐀𝐆𝐎 𝐂𝐍𝐏𝐉 300,00
😈🔥𝐀𝐌𝐄 𝐃𝐈𝐆𝐈𝐓𝐀𝐋 𝐂𝐍𝐏𝐉 200,00
😈🔥𝐒𝐀𝐌𝐔𝐏 𝐂𝐍𝐏𝐉 200,00 
😈🔥𝐁𝐄𝐒𝐒 𝐁𝐀𝐍𝐊 𝐂𝐍𝐏𝐉 200,00
😈🔥𝐑𝐄𝐂𝐀𝐑𝐆𝐀𝐏𝐀𝐘 𝐂𝐍𝐏𝐉 250,00</b>""",
  reply_markup=kb,
    )



@Client.on_callback_query(filters.regex(r"^history$"))
async def history(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
        
       [ InlineKeyboardButton("💳 Historico de Contas Premium", callback_data="buy_history_contas")
        ],
            [
                InlineKeyboardButton("❮ ❮", callback_data="user_info"),
            ],
        ]
    )
    await m.edit_message_text(
        f"""⚠️ Selecione qual historico de compras você deseja ver.</b>""",
        reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"^buy_history$"))
async def buy_history(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("❮ ❮", callback_data="history"),
            ],
        ]
    )
    history = cur.execute(
        "SELECT nome, cpf, linkdoc, bought_date , level, score ,localidade FROM docs_sold WHERE owner = ? ORDER BY bought_date DESC LIMIT 50",
        [m.from_user.id],
    ).fetchall()

    if not history:
        cards_txt = "<b>⚠️ Não há nenhuma compra nos registros.</b>"
    else:
        documentos = []
        print(documentos)
        for card in history:
            documentos.append("|".join([i for i in card]))
        cards_txt = "\n".join([f"<code>{cds}</code>" for cds in documentos])

    await m.edit_message_text(
        f"""<b>🛒 Histórico de compras</b>
<i>- Histórico de 50 últimas compras.</i>
NOME|CPF|LINK|COMPRADO|TIPO|SCORE|CIDADE

{cards_txt}""",
        reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"^buy_history_contas$"))
async def buy_history_contas(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("❮ ❮", callback_data="history"),
            ],
        ]
    )
    history = cur.execute(
        "SELECT tipo, email, senha, cidade bought_date FROM contas_sold WHERE owner = ? ORDER BY bought_date DESC LIMIT 50",
        [m.from_user.id],
    ).fetchall()

    if not history:
        cards_txt = "<b>⚠️ Não há nenhuma compra nos registros.</b>"
    else:
        documentos = []
        print(documentos)
        for card in history:
            documentos.append("|".join([i for i in card]))
        cards_txt = "\n".join([f"<code>{cds}</code>" for cds in documentos])

    await m.edit_message_text(
        f"""<b>🛒 Histórico de compras</b>
<i>- Histórico de 50 últimas compras.</i>
TIPO|EMAIL|SENHA|CIDADE|COMPRADO

{cards_txt}""",
        reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"^buy_history_log$"))
async def buy_history_log(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("❮ ❮", callback_data="history"),
            ],
        ]
    )
    history = cur.execute(
        "SELECT tipo, email, senha, cidade bought_date FROM logins_sold WHERE owner = ? ORDER BY bought_date DESC LIMIT 50",
        [m.from_user.id],
    ).fetchall()

    if not history:
        cards_txt = "<b>⚠️ Não há nenhuma compra nos registros.</b>"
    else:
        documentos = []
        print(documentos)
        for card in history:
            documentos.append("|".join([i for i in card]))
        cards_txt = "\n".join([f"<code>{cds}</code>" for cds in documentos])

    await m.edit_message_text(
        f"""<b>🛒 Histórico de compras</b>
<i>- Histórico de 50 últimas compras.</i>
TIPO|EMAIL|SENHA|CIDADE|COMPRADO

{cards_txt}""",
        reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"^buy_history_vales$"))
async def buy_history_vales(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("❮ ❮", callback_data="history"),
            ],
        ]
    )
    history = cur.execute(
        "SELECT tipo, email, senha, cpf,limite,cidade bought_date FROM vales_sold WHERE owner = ? ORDER BY bought_date DESC LIMIT 50",
        [m.from_user.id],
    ).fetchall()

    if not history:
        cards_txt = "<b>⚠️ Não há nenhuma compra nos registros.</b>"
    else:
        documentos = []
        print(documentos)
        for card in history:
            documentos.append("|".join([i for i in card]))
        cards_txt = "\n".join([f"<code>{cds}</code>" for cds in documentos])

    await m.edit_message_text(
        f"""<b>🛒 Histórico de compras</b>
<i>- Histórico de 50 últimas compras.</i>
TIPO|EMAIL|SENHA|CPF|LIMIE|CIDADE|COMPRADO

{cards_txt}""",
        reply_markup=kb,
    )
    
@Client.on_callback_query(filters.regex(r"^buy_history_cc$"))
async def buy_history_cc(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("🔙 Voltar", callback_data="user_info"),
            ],
        ]
    )
    history = cur.execute(
        "SELECT number, month, year, cvv FROM cards_sold WHERE owner = ? ORDER BY bought_date DESC LIMIT 50",
        [m.from_user.id],
    ).fetchall()

    if not history:
        cards_txt = "<b>Não há nenhuma compra nos registros.</b>"
    else:
        cards = []
        for card in history:
            cards.append("|".join([i for i in card]))
        cards_txt = "\n".join([f"<code>{cds}</code>" for cds in cards])

    await m.edit_message_text(
        f"""<b>💳 Histórico de compras de ccs</b>
<i>- Histórico de 50 últimas compras.</i>

{cards_txt}""",
        reply_markup=kb,
    )
    
@Client.on_callback_query(filters.regex(r"^buy_history_gg$"))
async def buy_history(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("🔙 Voltar", callback_data="history"),
            ],
        ]
    )
    history = cur.execute(
        "SELECT number, month, year, cvv FROM ggs_sold WHERE owner = ? ORDER BY bought_date DESC LIMIT 50",
        [m.from_user.id],
    ).fetchall()

    if not history:
        cards_txt = "<b>Não há nenhuma compra nos registros.</b>"
    else:
        cards = []
        for card in history:
            cards.append("|".join([i for i in card]))
        cards_txt = "\n".join([f"<code>{cds}</code>" for cds in cards])

    await m.edit_message_text(
        f"""<b>💳 Histórico de compras de ggs</b>
<i>- Histórico de 50 últimas compras.</i>

{cards_txt}""",
        reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"^buy_history_cons$"))
async def buy_history_cons(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("❮ ❮", callback_data="history"),
            ],
        ]
    )
    history = cur.execute(
        "SELECT limite, preco, anjo, token,cc,bincc,senha,mes,ano,cvv,cpf,telefone,nome,nomebanco bought_date FROM consul_solds WHERE owner = ? ORDER BY bought_date DESC LIMIT 50",
        [m.from_user.id],
    ).fetchall()

    if not history:
        cards_txt = "<b>⚠️ Não há nenhuma compra nos registros.</b>"
    else:
        documentos = []
        print(documentos)
        for card in history:
            documentos.append("|".join([i for i in card]))
        cards_txt = "\n".join([f"<code>{cds}</code>" for cds in documentos])

    await m.edit_message_text(
        f"""<b>🛒 Histórico de compras de consul</b>
<i>- Histórico de 50 últimas compras.</i>

{cards_txt}""",
        reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"^swap$"))
async def swap_points(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("⬅️ Voltar", callback_data="start"),
            ],
        ]
    )

    user_id = m.from_user.id
    balance, diamonds = cur.execute(
        "SELECT balance, balance_diamonds FROM users WHERE id=?", [user_id]
    ).fetchone()

    if diamonds >= 10:
        add_saldo = round((diamonds / 2), 2)
        new_balance = round((balance + add_saldo), 2)

        txt = f"⚜️ Seus <b>{diamonds}</b> pontos foram convertidos em R$ <b>{add_saldo}</b> de saldo."

        cur.execute(
            "UPDATE users SET balance = ?, balance_diamonds=?  WHERE id = ?",
            [new_balance, 0, user_id],
        )
        return await m.edit_message_text(txt, reply_markup=kb)

    await m.answer(
        "⚠️ Você não tem pontos suficientes para realizar a troca. O mínimo é 10 pontos.",
        show_alert=True,
    )


   
@Client.on_callback_query(filters.regex(r"^swap_info$"))
async def swap_info(c: Client, m: CallbackQuery):
    await m.message.delete()

    cpf = await m.message.ask(
        "<b>👤 CPF da lara (exemplo: 12345678901)</b>",
        reply_markup=ForceReply(),
        timeout=120,
    )
    name = await m.message.ask(
        "<b>👤 Nome completo do pagador (exemplo: jacinto pinto)</b>", reply_markup=ForceReply(), timeout=120
    )
    email = await m.message.ask(
        "<b>📧 E-mail (exemplo: abcd@gmail.com)</b>", reply_markup=ForceReply(), timeout=120
    )
    cpf, name, email = cpf.text, name.text, email.text
    cur.execute(
        "UPDATE users SET cpf = ?, name = ?, email = ?  WHERE id = ?",
        [cpf, name, email, m.from_user.id],
    )
    save()

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("⬅️ Voltar", callback_data="start"),
            ]
        ]
    )
    await m.message.reply_text(
        "<b> ✅ Seus dados foram alterados com sucesso.</b>", reply_markup=kb
    )