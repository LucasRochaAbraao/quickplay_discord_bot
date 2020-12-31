import os
import json
import random
import datetime
import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
#from dotenv import load_dotenv

#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = os.environ["DISCORD_TOKEN"]

cluster = MongoClient(os.environ["DB_URL"])
db = cluster['quickplay_db']
collection = db["discord"]

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=('!', '$'), description="QuickPlay Bot", intents=intents, case_insensitive=True)
bot.remove_command("help") # eu faço um melhor abaixo

meme_imgs = [
    'https://img_a.jpg',
    'https://img_b.jpg'
    'https://img_c.jpg'
]

@bot.group(invoke_without_command=True)
async def ajuda(ctx):
    emb = discord.Embed(title = "Ajuda", description = "Use !ajuda <comando> para mais informações sobre algum comando específico.", color = ctx.author.color)
    emb.add_field(name = "Membros", value = "regras|regra, info, saldo, brinde, enviar_qbits")
    emb.add_field(name = "Admin", value = "limpar, kick, ban")
    await ctx.send(embed = emb)

@ajuda.command()
async def info(ctx):
    emb = discord.Embed(title = "Info", description = "Mostra informações de um membro", color = ctx.author.color)
    emb.add_field(name = "**sintaxe**", value = "!info <membro>")
    await ctx.send(embed = emb)

@ajuda.command()
async def regras(ctx):
    emb = discord.Embed(title = "Regras", description = "Mostra todas as regras do servidor.", color = ctx.author.color)
    emb.add_field(name = "**sintaxe**", value = "!regras")
    await ctx.send(embed = emb)

@ajuda.command()
async def regra(ctx):
    emb = discord.Embed(title = "Regras", description = "Mostra a regra solicitada.", color = ctx.author.color)
    emb.add_field(name = "**sintaxe**", value = "!regra <nº da regra>")
    await ctx.send(embed = emb)

@ajuda.command()
async def limpar(ctx):
    emb = discord.Embed(title = "Limpar", description = "Deleta mensagens recentes", color = ctx.author.color)
    emb.add_field(name = "**sintaxe**", value = "!limpar [quantidade]")
    await ctx.send(embed = emb)

@ajuda.command()
async def kick(ctx):
    emb = discord.Embed(title = "Kick", description = "Retira um membro do servidor", color = ctx.author.color)
    emb.add_field(name = "**sintaxe**", value = "!kick <membro> [razão]")
    await ctx.send(embed = emb)

@ajuda.command()
async def ban(ctx):
    emb = discord.Embed(title = "Ban", description = "Banir um membro do servidor", color = ctx.author.color)
    emb.add_field(name = "**sintaxe**", value = "!ban <membro> [razão]")
    await ctx.send(embed = emb)

@ajuda.command()
async def saldo(ctx):
    emb = discord.Embed(title = "Saldo", description = "Consultar saldo de qBits de um usuário", color = ctx.author.color)
    emb.add_field(name = "**sintaxe**", value = "!saldo [membro]")
    await ctx.send(embed = emb)

@ajuda.command()
async def brinde(ctx):
    emb = discord.Embed(title = "Brinde", description = "Solicitar um brinde de qBits", color = ctx.author.color)
    emb.add_field(name = "**sintaxe**", value = "!saldo [membro]")
    await ctx.send(embed = emb)

# =================================== EVENTS =================================== #

@bot.event
async def on_ready():
    #print(f'{bot.user.name} se conectou ao servidor {dir(bot.user)}!')
    #print(f'{bot.user.name}:{bot.user.id} se conectou ao servidor!')
    print(f'{bot.user.name} se conectou ao servidor!')
    return await bot.change_presence(activity=discord.Activity(type=1, name='Quick Play', url='https://www.youtube.com/channel/UCNaWl0HNSmDk4fO8NQBii4Q'))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para isso espertinho!")
        #await ctx.message.delete()
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Por favor, coloque todos parâmetros")
        #await ctx.message.delete()
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Não entendi esse comando :/")
        #await ctx.message.delete()
    else:
        raise error

@bot.event
async def on_message(msg):
    await filtrar_palavras(msg)
    await processar_xp(msg)

    await bot.process_commands(msg)

@bot.event
async def on_message_delete(msg):
    ''' Mensagem no canal ao detectar uma mensagem deletada.'''
    #print("peguei") #debug no console
    # futuramente, caso seja necessário, posso criar um log com mensagens deletadas (autor, data, etc)
    #await msg.channel.send('Deus leu o que você apagou!')

@bot.event
async def on_member_join(member):
    ''' Mensagem de boas vindas privada.'''
    #print(dir(member))
    await member.send('Olá! Seja bem vindo ao servidor discord Quick Play!')# Fique atento para instruções no processo de inscrição do primeiro campeonato Quick Play de LOL!')

# ==== helper funcions ==== #
async def filtrar_palavras(msg):
    with open("resources/palavras_filtradas.txt", "r") as arq:
        palavras_filtradas = arq.readlines()
        for word in palavras_filtradas:
            if word in msg.content:
                await msg.delete()

async def processar_xp(msg):
    sujeito = msg.author
    pesquisa = collection.find_one({"_id": sujeito.id})
    if pesquisa:
        collection.update_one({"_id": sujeito.id}, {"$inc": {"xp": random.randrange(3, 5)}})
    else:
        collection.insert_one({"_id": sujeito.id, "username": sujeito.name, "xp": 0, "qbits": 25})

# =============================== COMANDOS COMUNS =============================== #

@bot.command(aliases=["usuario", "perfil"], help='Exibir um cartão (embed) com \
informações do usuário, incluindo sua carteira virtual com moedas q-bits.')
#@commands.has_permissions(kick_members = True) # caso seja necessário
async def info(ctx, member: discord.Member = None):
    if member:
        sujeito = member
    else:
        sujeito = ctx.author
    
    emb = discord.Embed(
        title = sujeito.name,
        timestamp = datetime.datetime.utcnow(),
        description = sujeito.mention,
        color = discord.Color.orange()
    )

    emb.add_field(name = "Membro desde", value = f"{sujeito.joined_at.strftime('%d-%m-%y')}")
    emb.add_field(name = "XP", value = await saldo_qbits_xp(sujeito, "xp"))
    emb.add_field(name = "qBits", value = await saldo_qbits_xp(sujeito, "qbits"))
    emb.set_thumbnail(url = sujeito.avatar_url)
    emb.set_footer(text="QUICK PLAY", icon_url="http://www.quick.com.br//images/logo-quick.png")
    await ctx.send(embed=emb)

@bot.command()
async def regra(ctx, *, num):
    regras_txt = get_regras()
    await ctx.send(regras_txt[int(num)-1])

@bot.command()
async def regras(ctx):
    regras_txt = get_regras()
    for reg in regras_txt:
        await ctx.send(reg)

# ----- funções internas ----- #
def get_regras():
    with open("resources/regras.txt", "r") as arq:
        regras_txt = arq.readlines()
    return regras_txt

# =============================== COMANDOS ADMIN ================================ #

@bot.command(name='limpar', aliases=["clear"], no_pm=True)
#@commands.has_permissions(manage_messages = True)
@commands.has_role('Admin')
async def limpar(ctx, amount=None):
    if amount is None:
        await ctx.channel.purge(limit=6)
    elif amount == "todas":
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=int(amount)+1)

@bot.command(aliases=["retirar"])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason = "Nenhum motivo foi providenciado"):
    await member.send(f"Você foi retirado pelo motivo:\n{reason}")
    await member.kick(reason=reason)

@bot.command(aliases=["banir"])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason = "Nenhum motivo foi providenciado"):
    await member.send(f"{member.name} foi banido pelo motivo:\n{reason}")
    await member.ban(reason=reason)

# ===================== COMANDOS DE GERENCIAMENTO FINANCEIRO ==================== #


@bot.command()
@commands.has_role('Admin')
async def brinde(ctx, member: discord.Member = None):
    if member:
        sujeito = member
    else:
        sujeito = ctx.author
    ganhos = random.randrange(3, 7)
    pesquisa = collection.find_one({"_id": sujeito.id})
    if pesquisa:
        collection.update_one({"_id": sujeito.id}, {"$inc": {"qbits": ganhos}})
        await ctx.send(f"@{sujeito.name} recebeu {ganhos} qBits!")
    else:
        collection.insert_one({"_id": sujeito.id, "username": sujeito.name, "xp": 0, "qbits": 25})
        await ctx.send(f"@{sujeito.name} não tinha conta qBits. Criamos uma para ele, e agora ele tem {ganhos} qBits!")

@bot.command()
@commands.has_role('Admin')
async def retirar_qbits(ctx, member: discord.Member = None, amount = None): # check if this works, otherwise cast to int
    amount = int(amount)
    if amount == None:
        await ctx.send("Por favor, selecione uma quantia.")
        return
    if member:
        sujeito = member
    else:
        sujeito = ctx.author

    pesquisa = collection.find_one({"_id": sujeito.id})
    if pesquisa:
        if amount > pesquisa["qbits"]:
            await ctx.send(f"@{sujeito.name} tem menos do que isso!")
            return
        if amount < 0:
            await ctx.send("Quantia precisa ser positiva!")
            return
        collection.update_one({"_id": sujeito.id}, {"$inc": {"qbits": -amount}})
        await ctx.send(f"Você retirou {amount} qBits de @{sujeito.name}!")
        return
    
    collection.insert_one({"_id": sujeito.id, "username": sujeito.name, "xp": 0, "qbits": 25})
    await ctx.send(f"@{sujeito.name} não possuía conta no banco. Acabamos de criar uma nova, com 25 qbits!")

@bot.command()
@commands.has_role('Admin')
async def depositar(ctx, member: discord.Member = None, amount: int = None):
    if amount == None:
        await ctx.send("Por favor, selecione uma quantia.")
        return
    if amount < 1:
        await ctx.send("Por favor, selecione uma quantia positiva para depositar!")
        return
    pesquisa = collection.find_one({"_id": member.id})
    if pesquisa:
        collection.update_one({"_id": member.id}, {"$inc": {"qbits": amount}})
        await ctx.send(f"@{member.name} recebeu {amount} qBits!")
    else:
        collection.insert_one({"_id": member.id, "username": member.name, "xp": 0, "qbits": amount})
        await ctx.send(f"@{member.name} não possuía conta no banco. Acabamos de criar uma nova, com {amount} qbits!")

@bot.command()
async def enviar_qbits(ctx, membro: discord.Member, amount = None):
    amount = int(amount)
    if amount < 1 or amount == None:
        await ctx.send("Por favor, selecione uma quantia positiva para enviar!")
        return
    remetente = collection.find_one({"_id": ctx.author.id})
    if remetente == None:
        collection.insert_one({"_id": ctx.author.id, "username": ctx.author.name, "xp": 0, "qbits": amount})
    destinatario = collection.find_one({"_id": membro.id})
    if destinatario == None:
        collection.insert_one({"_id": membro.id, "username": membro.name, "xp": 0, "qbits": amount})

    if amount > remetente["qbits"]:
        await ctx.send(f"Você não tem saldo suficiente para enviar {amount} qbits!")
        return
    
    collection.update_one({"_id": ctx.author.id}, {"$inc": {"qbits": -amount}})
    collection.update_one({"_id": membro.id}, {"$inc": {"qbits": amount}})
    await ctx.send(f"@{ctx.author.name} enviou {amount} qBits para @{membro.name}!")

# ----- funções internas ----- #

async def saldo_qbits_xp(membro: discord.Member, modo):
    pesquisa = collection.find_one({"_id": membro.id})
    if pesquisa: # caso o usuario exista, retorna o valor de qbits
        return pesquisa[modo]
    collection.insert_one({"_id": membro.id, "username": membro.name, "xp": 0, "qbits": 25})
    if modo == "xp":
        return 0
    else: # qbits padrão
        return 25 # caso contrário, insira o usuário na mongodb e retorna o valor inicial.

# ========================= COMANDOS EM DESENVOLVIMENTO ========================= #

bot.run(TOKEN)

"""
# por enquanto, não vejo necessidade disso, mais fácil fazer manual msm...
@bot.command(name='criar-canal', help='criar canal com nome personalizado.')
@commands.has_role('Admin')
async def create_channel(ctx, channel_name='canal-sem-nome'):
    existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Criando o canal "{channel_name}".')
        await ctx.guild.create_text_channel(name=channel_name)

@bot.command(name='deletar-canal', help='deleta o canal especificado')
@commands.has_role('Admin')
async def delete_channel(ctx, channel_name):
   # check if the channel exists
   existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
   # if the channel exists
   if existing_channel is not None:
      await existing_channel.delete()
   # if the channel does not exist, inform the user
   else:
      await ctx.send(f'Nenhum canal "{channel_name}" foi encontrado')

# desnecessário...
@bot.command(name='socorro', help='Enviar pergunta destacada para os Administradores.')
async def socorro(ctx, mensagem):
    await ctx.send(f"Admins, ele disse: {mensagem}")
"""
"""
# será implementado futuramente...
@bot.command(name='cor', help='Troca a cor do cartão (embed) do membro que tem\
essa função liberada.')
async def cor(ctx, cor_escolhida):
    await ctx.send(f"Nova cor do cartão: {cor_escolhida}")

@bot.command(aliases=[""]) # esse veio do canal do swastik no youtube
async def meme(ctx):
    emb = discord.Embed(color = discord.Color.red())
    random_link = random.choice(memes_img)
    emb.set_image(url = random_link)
    await ctx.send(embed=emb)

@bot.command(name='piada', help='Com esse comando liberado, o membro pode\
solicitar 3 piadas a cada 10 minutos.')
async def piada(ctx):
    await ctx.send("Alguma piada")

@bot.command(name='conselho', help='Com esse comando liberado, o membro pode\
solicitar 3 conselhos a cada 10 minutos.')
async def conselho(ctx):
    await ctx.send("Algum conselho")

@bot.command(name='contar-piada', help='Com esse comando liberado, o membro\
pode contar piadas ilimitada no canal aberto do servidor.')
async def contar_piada(ctx, piada):
    await ctx.send(piada)

@bot.command(name='aconselhar', help='Com esse comando liberado, o membro\
pode dar conselhos ilimitados no canal aberto do servidor.')
async def aconselhar(ctx, **kwargs):
    await ctx.send(kwags)

@bot.command(name='quick-tech', help='Gasta 100 q-bits para liberar o canal\
Quick-Tech, que contém conteúdo mensal sobre a internet, games e tecnologia.\
Esse custo serve para separá-lo do canal aberto, promovendo bate papo mais\
focado e sem spam.')
async def quick_tech(ctx):
    await ctx.send("Acesso liberado")
"""
"""
# comandos para campeonatos. À ser implementados.
@bot.command(name='registrar', help='Inicia o processo de se registrar\
em uma equipe.')
async def registrar(ctx):
    await ctx.send(f"Beleza {ctx.author.name}, vou te chamar no dm!")
    await ctx.author.send(f'Fala {ctx.author.name}, bora registrar sua equipe!\n\
\n\
Preciso que me envie a informação de cada jogador no seguinte formato:\n\
!registrar_integrante "equipe" "nome real" "nickname" "data de nascimento" \
"endereço" "email" "telefone de contato"\n\
\n\
Por exemplo: "!registrar_player "equipe" "Quick Fibra" "QuickPlay" \
"01/01/1998" "Rua Almirante Adalberto de barros Nunes 629, Vila Mury, VR, RJ" \
"suporte@quick.com.br" "(24) 3512 3312"')
# nome real
# nickname
# data de nascimento
# endereço
# email
# telefone de contato

@bot.command(name='registrar_integrante', help='Inscriçao de cada integrante da equipe.')
async def registrar_integrante(ctx, equipe, nome, nickname, dob, address, email, telefone):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        print(f"Equipe: {equipe}\nNome: {nome}\nNickname: {nickname}\n\
Data de nascimento: {dob}\nEndereço: {address}\nEmail: {email}\nTelefone: {telefone}")
        # json
        data = {equipe:{
            "nome completo": nome,
            "nickname": nickname,
            "data de nascimento": dob,
            "endereço": address,
            "email": email,
            "telefone": telefone
        }}
        print("criando arquivo json")
        with open(f"equipes/equipe_{equipe}_{nickname}.json", "w") as equipe_db:
            json.dump(data, equipe_db)
        print("pronto")

        await ctx.send("Jogador registrado!\nObs: para verificar os integrantes\
da sua equipe, use o comando: !minha_equipe.\nFaça a inscrição também no Battlefy: <link>")
    else:
        await ctx.send("Este comando funciona apenas no DM!")

@bot.command(name='minha_equipe', help='Inscriçao de cada integrante da equipe.')
async def minha_equipe(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(f"Info da equipe:\n-")
"""

"""
@bot.command(name='disregistrar', help='Remove sua inscrição de uma equipe.')
async def disregistrar(ctx):
    await ctx.send("De qual equipe?")

@bot.command(name='rodada', help='Informação sobre as partidas da rodada atual.')
async def rodada(ctx):
    await ctx.send("Partidas:")

@bot.command(name='equipe', help='Informação sobre sua equipe.')
async def equipe(ctx):
    await ctx.send("Cartão embed")

@bot.command(name='resultado', help='Resumo dos resultados dessa equipe.')
async def disregistrar(ctx, equipe):
    await ctx.send(f"Resultados da equipe {equipe}")

@bot.command(name='premio', help='Informação sobre a premiação.')
async def premio(ctx):
    await ctx.send("Regras de premiação:\n")

@bot.command(name='ping', help='Consultar status de saúde do bot.')
async def ping(ctx):
    await ctx.send("Bot ok! :D")

@bot.command(name='placar', help='Inicia o processo de registro de placar.')
async def placar(ctx, equipe_a, equipe_b):
    await ctx.send(f"Equipe {equipe_a[0]}: {equipe_a[1]}\nEquipe {equipe_b[0]}: {equipe_b[1]}")

@bot.command(name='nova_rodada', help='Inicia o processo de configuração\
da próxima rodada.')
async def nova_rodada(ctx):
    await ctx.send("Primeira partida?")

@bot.command(name='atribuir', help='Forma manual de atribuir q-bits ou troféis.')
async def atribuir(ctx, ativo, membro: discord.Member):
    await ctx.send(f"{ativo} entregue ao {membro.name}")

@bot.command(name='ban', help='Banir <membro>. OBS: comando de permissão ADMIN.')
async def ban(ctx, member : discord.Member = None, days = " ", reason = " "):
    '''Bans specified member from the server.'''
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await bot.say("Você não tem a role: Admin")
    pass

    try:
        if member == None:
            await bot.say(ctx.message.author.mention + ", Favor especificar um membro para banir!")
            return

        if member.id == ctx.message.author.id:
            await bot.say(ctx.message.author.mention + ", Você não pode se banir!")
            return
        else:
            await bot.ban(member, days)
            if reason == ".":
                await bot.say(member.mention + " Foi banido(a) do servidor!")
            else:
                await bot.say(member.mention + " Foi banido(a) do servidor! Razão: " + reason + ".")
            return
    except Forbidden:
        await bot.say("Você não tem as permissõe necessárias para banir alguém!")
        return
    except HTTPException:
        await bot.say("Algo deu errado, tente novamente mais tarde.")

@bot.command(name='kick', help='Retirar <membro>. OBS: comando de permissão ADMIN.')
async def kick(ctx, *, member : discord.Member = None):
    '''Kicks A User From The Server'''
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await bot.say("Você não tem a role: Admin")
    pass

    if not member:
        return await bot.say(ctx.message.author.mention + "Favor especificar um membro para kick!")
    try:
        await bot.kick(member)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            return await bot.say(":x: Privilégio muito baixo!")
 
    embed = discord.Embed(description = f"**{member.name}** foi retirado.", color = 0xF00000)
    embed.set_footer(text="QUICK GAMES", icon_url="https://is4-ssl.mzstatic.com/image/thumb/Purple113/v4/48/cd/fc/48cdfc22-cce0-9231-dfd9-2cc8c5661940/source/512x512bb.jpg")
    await bot.say(embed = embed)

#Mutes a Member From The server

@bot.command(name='silenciar', help='Silenciar <membro>. OBS: comando de permissão ADMIN.')
async def mute(ctx, *, member : discord.Member):
    '''Mutes A Memeber'''
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await bot.say("Você não tem a role: Admin")
    pass

    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    await bot.edit_channel_permissions(ctx.message.channel, member, overwrite)

    await bot.say(f"**{member.mention}** foi silenciado! Aguarde até ser liberado...")

#Unmutes a member

@bot.command(name='disilenciar', help='Tirar o silencio de <membro>. OBS: comando de permissão ADMIN.')
async def unmute(ctx, *, member : discord.Member):
    '''Unmutes The Muted Memeber'''
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await bot.say("Você não tem a role: Admin")
    pass

    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = True
    await bot.edit_channel_permissions(ctx.message.channel, member, overwrite)

    await bot.say(f"**{member.mention}** Pronto... Foi retirado do silêncio!")

######################################## MONGODB QUICK CHEATSHEET ######################################
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://quickplay:N0cqu1cK22@quickplay-discordbot-cl.pm3fu.mongodb.net/test")

db = cluster['quickplay_db']

collection = db['discord']

usuario = {"_id": "12345", "xp": 0, "qbits": 25}

usuario_id = collection.insert_one(usuario).inserted_id

pesquisa = collection.find_one({"_id": usuario_id})

novo = 7
collection.update_one({"_id": usuario_id}, {"$inc": {"qbits": novo}})


"""
