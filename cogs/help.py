import discord
from discord.ext import commands

class HelpCog(commands.Cog, name = "Ajuda"):
    """Comandos disponíveis para todos membros do servidor."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def ajuda(self, ctx):
        emb = discord.Embed(title = "Ajuda", description = "Use !ajuda <comando> para mais informações sobre algum comando específico.\nOBS: <obrigatório> e [opcional]", color = ctx.author.color)
        emb.add_field(name = "Membros", value = "regras|regra, info, brinde, enviar_qbits")
        emb.add_field(name = "Admin", value = "limpar, kick, ban, depositar, retirar_qbits")
        await ctx.send(embed = emb)

    @ajuda.command(name="info")
    async def _info(self, ctx):
        emb = discord.Embed(title = "Info", description = "Mostrar suas informações ou de um membro.", color = ctx.author.color)
        emb.add_field(name = "**sintaxe**", value = "!info [membro]")
        await ctx.send(embed = emb)

    @ajuda.command(name="regras")
    async def _regras(self, ctx):
        emb = discord.Embed(title = "Regras", description = "Mostrar todas as regras do servidor.", color = ctx.author.color)
        emb.add_field(name = "**sintaxe**", value = "!regras")
        await ctx.send(embed = emb)

    @ajuda.command(name="regra")
    async def _regra(self, ctx):
        emb = discord.Embed(title = "Regra", description = "Mostrar a regra solicitada.", color = ctx.author.color)
        emb.add_field(name = "**sintaxe**", value = "!regra <nº da regra>")
        await ctx.send(embed = emb)

    @ajuda.command(name="limpar")
    async def _limpar(self, ctx):
        emb = discord.Embed(title = "Limpar", description = "[ADM] Deletar mensagens recentes.", color = ctx.author.color)
        emb.add_field(name = "**sintaxe**", value = "!limpar [quantidade]")
        await ctx.send(embed = emb)

    @ajuda.command(name="kick")
    async def _kick(self, ctx):
        emb = discord.Embed(title = "Kick", description = "[ADM] Retirar um membro do servidor.", color = ctx.author.color)
        emb.add_field(name = "**sintaxe**", value = "!kick <membro> [razão]")
        await ctx.send(embed = emb)

    @ajuda.command(name="ban")
    async def _ban(self, ctx):
        emb = discord.Embed(title = "Ban", description = "[ADM] Banir um membro do servidor.", color = ctx.author.color)
        emb.add_field(name = "**sintaxe**", value = "!ban <membro> [razão]")
        await ctx.send(embed = emb)

    @ajuda.command(name="brinde")
    async def _brinde(self, ctx):
        emb = discord.Embed(title = "Brinde", description = "Solicitar um brinde de qBits.", color = ctx.author.color)
        emb.add_field(name = "**sintaxe**", value = "!brinde [membro]")
        await ctx.send(embed = emb)

    @ajuda.command(name="enviar_qbits")
    async def _enviar_qbits(self, ctx):
        emb = discord.Embed(title = "Enviar_qbits", description = "Transferência de qBits da sua conta para outro membro.", color = ctx.author.color)
        emb.add_field(name = "**sintaxe**", value = "!enviar_qbits <membro> <valor>")
        await ctx.send(embed = emb)

    @ajuda.command(name="depositar")
    async def _depositar(self, ctx):
        emb = discord.Embed(title = "Depositar", description = "[ADM] Deposita qualquer quantia de qBits para um membro.", color = ctx.author.color)
        emb.add_field(name = "**sintaxe**", value = "!depositar <membro> <valor>")
        await ctx.send(embed = emb)

    @ajuda.command(name="retirar_qbits")
    async def _retirar_qbits(self, ctx):
        emb = discord.Embed(title = "Retirar_qbits", description = "[ADM] Retira qualquer quantia de qBits para um membro.", color = ctx.author.color)
        emb.add_field(name = "**sintaxe**", value = "!retirar_qbits [membro] <valor>")
        await ctx.send(embed = emb)

def setup(bot):
    bot.add_cog(HelpCog(bot))
