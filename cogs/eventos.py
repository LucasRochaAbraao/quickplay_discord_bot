import os
import random
import discord
from discord.ext import commands

class EventsCog(commands.Cog, name = "Eventos"):
    """ Docstrings (Cog Description) """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} se conectou ao servidor!')
        await self.bot.change_presence(activity=random.choice([
            discord.Activity(type=1, name='QUICKPLAY', url='https://www.youtube.com/channel/UCNaWl0HNSmDk4fO8NQBii4Q'),
            discord.Streaming(name="QUICKPLAY", url="")
        ]))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Você não tem permissão para isso espertinho!")
            #await ctx.message.delete()
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Por favor, coloque todos parâmetros.")
            #await ctx.message.delete()
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("Não entendi esse comando. :/\n!ajuda para comandos disponíveis.")
            #await ctx.message.delete()
        else:
            raise error

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user:
            return
        await self.filtrar_palavras(msg)
        await self.processar_xp(msg) # Acredito ser desnecessário

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        ''' Mensagem no canal ao detectar uma mensagem deletada.'''
        print(f"{msg.author.name} apagou: {msg.content}") #debug no console, ainda não testei
        # futuramente, caso seja necessário, posso criar um log com mensagens deletadas (autor, data, etc)
        await msg.channel.send(content=f"@{msg.author.name}", file=discord.File("resources/msg_on_delete.png"))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        ''' Mensagem de boas vindas privada.'''
        await member.send('Olá! Seja bem vindo ao servidor discord QUICKPLAY!')
        #caso queira mensagem pública:
        #channel = member.guild.system_channel # this channel can be set in server config
        #if channel is not None:
        #    await channel.send(f'Bem vindo {member.mention}.')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        if message_id == 804046030562918440: # specific message in the server
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds) # this guild only

            if payload.emoji.name == 'some_emoji': # only if role != emoji name
                role = discord.utils.get(guild.roles, name="actual_name")
            else:
                role = discord.utils.get(guild.roles, name=payload.emoji.name)
            
            if role is not None:
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)
                    print(f"Added {role} role to {member.name}")
                else:
                    print(f"Member {member.name} not found.")
            else:
                print(f"Role {role} not found.")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id
        if message_id == 804046030562918440: # specific message in the server
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds) # this guild only

            if payload.emoji.name == 'some_emoji': # only if role != emoji name
                role = discord.utils.get(guild.roles, name="actual_name")
            else:
                role = discord.utils.get(guild.roles, name=payload.emoji.name)
            
            if role is not None:
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
                    print(f"Removed {role} role from {member.name}")
                else:
                    print(f"Member {member.name} not found.")
            else:
                print(f"Role {role} not found.")

    # ==== helper methods ==== #
    async def filtrar_palavras(self, msg):
        current_directory = os.path.dirname(__file__)
        parent_directory = os.path.split(current_directory)[0]
        file_path = os.path.join(parent_directory, 'resources', 'palavras_filtradas.txt')
        with open(file_path, "r") as arq:
            palavras_filtradas = arq.readlines()
            for word in palavras_filtradas:
                if word in msg.content:
                    await msg.delete()

    #Antes de cogs e ficava tudo em 1 arquivo, essa função tinha acesso ao mongodb
    async def processar_xp(self, msg):
        economy = self.bot.get_cog('Nível e Economia')
        if economy is not None:
            coll = economy.collection
        sujeito = msg.author
        pesquisa = coll.find_one({"_id": sujeito.id})
        if pesquisa:
            coll.update_one({"_id": sujeito.id}, {"$inc": {"xp": random.randrange(3, 5)}})
        else:
            coll.insert_one({"_id": sujeito.id, "username": sujeito.name, "xp": 0, "qbits": 25})


def setup(bot):
    bot.add_cog(EventsCog(bot))
