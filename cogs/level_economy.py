import os
import datetime
import random
import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient

class LevelEconomyCog(commands.Cog, name='Nível e Economia'):
    """ Docstrings (Cog Description)
    COMANDOS DE GERENCIAMENTO FINANCEIRO """

    def __init__(self, bot):
        self.bot = bot
        self.cluster = MongoClient(os.environ["DB_URL"])
        self.db = self.cluster['quickplay_db']
        self.collection = self.db["discord"]
        print(self.collection)
    
    @commands.command(aliases=["usuario", "perfil"], help='Exibir um cartão (embed) com \
    informações do usuário, incluindo sua carteira virtual com moedas q-bits.')
    async def info(self, ctx, member: discord.Member = None):
        sujeito = member if member else ctx.author
                
        emb = discord.Embed(
            title = sujeito.name,
            timestamp = datetime.datetime.utcnow(),
            description = sujeito.mention,
            color = discord.Color.orange()
        )

        emb.add_field(name = "Membro desde", value = f"{sujeito.joined_at.strftime('%d-%m-%y')}")
        emb.add_field(name = "XP", value = await self.saldo_qbits_xp(sujeito, "xp"))
        emb.add_field(name = "qBits", value = await self.saldo_qbits_xp(sujeito, "qbits"))
        emb.set_thumbnail(url = sujeito.avatar_url)
        emb.set_footer(text="QUICK PLAY", icon_url="http://www.quick.com.br//images/logo-quick.png")
        await ctx.send(embed=emb)

    #@commands.command(pass_context=True)
    #@commands.has_role('Admin')
    @commands.command()
    async def brinde(self, ctx, member: discord.Member = None):
        sujeito = member if member else ctx.author
        ganhos = random.randrange(3, 7)
        pesquisa = self.collection.find_one({"_id": sujeito.id})
        if pesquisa:
            self.collection.update_one({"_id": sujeito.id}, {"$inc": {"qbits": ganhos}})
            await ctx.send(f"@{sujeito.name} recebeu {ganhos} qBits!")
        else:
            self.collection.insert_one({"_id": sujeito.id, "username": sujeito.name, "xp": 0, "qbits": 25})
            await ctx.send(f"@{sujeito.name} não tinha conta qBits. Criamos uma para ele, e agora ele tem {ganhos} qBits!")

    @commands.command()
    @commands.has_role('Admin')
    async def retirar_qbits(self, ctx, member: discord.Member = None, amount = None):
        if amount == None:
            await ctx.send("Por favor, selecione uma quantia.")
            return
        amount = int(amount)
        
        sujeito = member if member else ctx.author

        pesquisa = self.collection.find_one({"_id": sujeito.id})
        if pesquisa:
            if amount > pesquisa["qbits"]:
                await ctx.send(f"@{sujeito.name} tem menos do que isso!")
                return
            if amount < 0:
                await ctx.send("Quantia precisa ser positiva!")
                return
            self.collection.update_one({"_id": sujeito.id}, {"$inc": {"qbits": -amount}})
            await ctx.send(f"Você retirou {amount} qBits de @{sujeito.name}!")
            return
        
        self.collection.insert_one({"_id": sujeito.id, "username": sujeito.name, "xp": 0, "qbits": 25})
        await ctx.send(f"@{sujeito.name} não possuía conta no banco. Acabamos de criar uma nova, com 25 qbits!")

    @commands.command()
    @commands.has_role('Admin')
    async def depositar(self, ctx, amount: int = None, member: discord.Member = None):
        if amount == None:
            await ctx.send("Por favor, selecione uma quantia.")
            return
        if amount < 1:
            await ctx.send("Por favor, selecione uma quantia positiva para depositar!")
            return

        sujeito = member if member else ctx.author
        pesquisa = self.collection.find_one({"_id": member.id})
        if pesquisa:
            self.collection.update_one({"_id": sujeito.id}, {"$inc": {"qbits": amount}})
            await ctx.send(f"@{sujeito.name} recebeu {amount} qBits!")
        else:
            self.collection.insert_one({"_id": sujeito.id, "username": sujeito.name, "xp": 0, "qbits": amount})
            await ctx.send(f"@{sujeito.name} não possuía conta no banco. Acabamos de criar uma nova, com {amount} qbits!")

    @commands.command()
    async def enviar_qbits(self, ctx, membro: discord.Member, amount = None):
        if amount < 1 or amount == None:
            await ctx.send("Por favor, selecione uma quantia positiva para enviar!")
            return
        amount = int(amount)
        remetente = self.collection.find_one({"_id": ctx.author.id})
        if remetente == None:
            self.collection.insert_one({"_id": ctx.author.id, "username": ctx.author.name, "xp": 0, "qbits": amount})
        destinatario = self.collection.find_one({"_id": membro.id})
        if destinatario == None:
            self.collection.insert_one({"_id": membro.id, "username": membro.name, "xp": 0, "qbits": amount})

        if amount > remetente["qbits"]:
            await ctx.send(f"Você não tem saldo suficiente para enviar {amount} qbits!")
            return
        
        self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"qbits": -amount}})
        self.collection.update_one({"_id": membro.id}, {"$inc": {"qbits": amount}})
        await ctx.send(f"@{ctx.author.name} enviou {amount} qBits para @{membro.name}!")

    # ----- funções internas ----- #

    async def saldo_qbits_xp(self, membro: discord.Member, modo):
        pesquisa = self.collection.find_one({"_id": membro.id})
        if pesquisa: # caso o usuario exista, retorna o valor de qbits
            return pesquisa[modo]
        self.collection.insert_one({"_id": membro.id, "username": membro.name, "xp": 0, "qbits": 25})
        if modo == "xp":
            return 0
        else: # qbits padrão
            return 25 # caso contrário, insira o usuário na mongodb e retorna o valor inicial.


def setup(bot):
    bot.add_cog(LevelEconomyCog(bot))

"""
######################################## MONGODB QUICK CHEATSHEET ######################################
import pymongo
from pymongo import MongoClient

cluster = MongoClient("url")

db = cluster['quickplay_db']

collection = db['discord']

usuario = {"_id": "12345", "xp": 0, "qbits": 25}

usuario_id = collection.insert_one(usuario).inserted_id

pesquisa = collection.find_one({"_id": usuario_id})

novo = 7
collection.update_one({"_id": usuario_id}, {"$inc": {"qbits": novo}})

"""