import os
import datetime
import random
import discord
from discord.ext import commands

class LevelCog(commands.Cog, name='Level'):
    """ Docstrings (Cog Description)
    COMANDOS DE GERENCIAMENTO DE NIVELAMENTO """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ranking(self, ctx):

        # coll.find() retorna tudo: {'_id': ..., 'username': '...', 'xp': ..., 'qbits': ...}
        cursor = self.bot.collection.find()
        dados_iniciais = list()
        for dado in cursor:
            dados_iniciais.append(dado)

        dados_ordenados = sorted(dados_iniciais, key=lambda ordenar_by_xp: ordenar_by_xp['xp'])
        dados_ordenados.reverse() # a lista anterior é de menor pra maior
        await ctx.send(f"Os 10 primeiros são...\n{dados_ordenados[:10]}")

    # ----- funções internas ----- #

    async def saldo_qbits_xp(self, membro: discord.Member, modo):
        pesquisa = self.bot.collection.find_one({"_id": membro.id})
        if pesquisa: # caso o usuario exista, retorna o valor de qbits
            return pesquisa[modo]
        self.bot.collection.insert_one({"_id": membro.id, "username": membro.name, "xp": 0, "qbits": 25})
        if modo == "xp":
            return 0
        else: # qbits padrão
            return 25 # caso contrário, insira o usuário na mongodb e retorna o valor inicial.


def setup(bot):
    bot.add_cog(LevelCog(bot))

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

DB_URL="mongodb+srv://quickplay:N0cqu1cK22@quickplay-discordbot-cl.pm3fu.mongodb.net/test"
DISCORD_DB='quickplay_sqlite.db'
