import os
import datetime
import discord
from discord.ext import commands

class MembroCog(commands.Cog, name = "Membros"):
    """Comandos disponíveis para todos membros do servidor."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def regra(self, ctx, *, num):
        regras_txt, qnt = self.get_regras(1)
        if int(num) > qnt:
            await ctx.send(f"Nós temos apenas {qnt} regras por enquanto...")
            return
        await ctx.send(regras_txt[int(num)-1])

    @commands.command()
    async def regras(self, ctx):
        regras_txt = self.get_regras()
        for reg in regras_txt:
            await ctx.send(reg)

    # ----- funções internas ----- #
    def get_regras(qnt=None):
        current_directory = os.path.dirname(__file__)
        parent_directory = os.path.split(current_directory)[0]
        file_path = os.path.join(parent_directory, 'resources', 'regras.txt')
        with open(file_path, "r") as arq:
            regras_txt = arq.readlines()
        if qnt:
            return regras_txt, len(regras_txt)
        return regras_txt


def setup(bot):
    bot.add_cog(MembroCog(bot))
