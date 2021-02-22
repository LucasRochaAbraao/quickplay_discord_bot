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