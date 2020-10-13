import os
import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=('!', '$'), description="teste", intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    #print(f'{bot.user.name} se conectou ao servidor {dir(bot.user)}!')
    print(f'{bot.user.name}:{bot.user.id} se conectou ao servidor!')
    return await bot.change_presence(activity=discord.Activity(type=1, name='Quick Play', url='https://www.youtube.com/channel/UCNaWl0HNSmDk4fO8NQBii4Q'))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Você não tem permissão para esse comando, espertinho ;)')

@bot.event
async def on_message_delete(msg):
    ''' Mensagem no canal ao detectar uma mensagem deletada.'''
    await msg.channel.send('Deus leu o que você apagou!')

@bot.event
async def on_member_join(member):
    ''' Mensagem de boas vindas privada.'''
    print(dir(member))
    await member.send('Mensagem de boas vindas privada.')

@bot.command(name='perfil', help='Exibir um cartão (embed) com informações do usuário,\
incluindo sua carteira virtual com moedas q-bits.')
async def perfil(ctx, member: discord.Member):
    #print(dir(member))
    embed = discord.Embed(
        title=f"{member.name}", timestamp=datetime.datetime.utcnow(),
        color=discord.Color.orange()
    )
    embed.add_field(name="Membro desde:", value=f"{member.joined_at}")
    embed.add_field(name="ID:", value=f"{member.id}")
    embed.set_thumbnail(url=f"{member.avatar_url}")
    #embed.set_thumbnail(url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")
    #embed.set_image(url=f'{member.avatar_url}')
    embed.set_footer(text="QUICK GAMES", icon_url="https://is4-ssl.mzstatic.com/image/thumb/Purple113/v4/48/cd/fc/48cdfc22-cce0-9231-dfd9-2cc8c5661940/source/512x512bb.jpg")
    await ctx.send(embed=embed)

@bot.command(name='criar-canal', help='criar canal com nome personalizado.')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='canal-sem-nome'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Criando o canal: {channel_name}')
        await guild.create_text_channel(channel_name)

@bot.command(name='comandos', help='Resumo dos comandos disponíveis.')
async def comandos(ctx):
    await ctx.send("comandos disponíveis:\n1 - \n2 - ")

@bot.command(name='socorro', help='Enviar pergunta destacada para os Administradores.')
async def socorro(ctx, mensagem):
    await ctx.send(f"Admins, ele disse: {mensagem}")

@bot.command(name='cor', help='Troca a cor do cartão (embed) do membro que tem\
essa função liberada.')
async def cor(ctx, cor_escolhida):
    await ctx.send(f"Nova cor do cartão: {cor_escolhida}")

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

@bot.command(name='registrar', help='Inicia o processo de se registrar em uma equipe.')
async def registrar(ctx):
    await ctx.send("Em qual equipe?")

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

@bot.command(name='criar_equipe', help='Inicia o processo de criação de uma equipe.')
async def criar_equipe(ctx, nome, url):
    await ctx.send(f"Equipe {nome} criada com ícone personalizado.")

@bot.command(name='placar', help='Inicia o processo de registro de placar.')
async def placar(ctx, equipe_a, equipe_b):
    await ctx.send(f"Equipe {equipe_a[0]}: {equipe_a[1]}\nEquipe {equipe_b[0]}: {equipe_b[1]}")

@bot.command(name='nova_rodada', help='Inicia o processo de configuração\
da próxima rodada.')
async def nova_rodada(ctx):
    await ctx.send("Primeira partida?")

@bot.command(name='atribuir', help='Forma manual de atribuir q-bits ou troféis.')
async def atribuir(ctx, ativo, membro):
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


bot.run(TOKEN)
