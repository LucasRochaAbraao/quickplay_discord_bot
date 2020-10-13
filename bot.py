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

@bot.command(name='info', help='informação sobre um membro.')
async def info(ctx, member: discord.Member):
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

@bot.command(name='soma', help='escolha 2 números para serem somados.')
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)

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

@bot.command(name='mute', help='Mutar <membro>. OBS: comando de permissão ADMIN.')
async def mute(ctx, *, member : discord.Member):
    '''Mutes A Memeber'''
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await bot.say("Você não tem a role: Admin")
    pass

    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    await bot.edit_channel_permissions(ctx.message.channel, member, overwrite)

    await bot.say(f"**{member.mention}** foi mutado! Aguarde até ser liberado...")

#Unmutes a member

@bot.command(name='unmute', help='Tirar o mute de <membro>. OBS: comando de permissão ADMIN.')
async def unmute(ctx, *, member : discord.Member):
    '''Unmutes The Muted Memeber'''
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await bot.say("Você não tem a role: Admin")
    pass

    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = True
    await bot.edit_channel_permissions(ctx.message.channel, member, overwrite)

    await bot.say(f"**{member.mention}** Pronto... Foi retirado seu mute!")


bot.run(TOKEN)
