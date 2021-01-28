import discord
from discord.ext import commands

class AdminCog(commands.Cog, name = "Admin"):
    """ Docstrings (Cog Description)
    Comandos de membros Administradores """

    def __init__(self, bot):
        self.bot = bot

    #@commands.command(pass_context=True)
    @commands.command(name='limpar', aliases=["clear"], no_pm=True)
    @commands.has_role('Admin')
    async def limpar(self, ctx, amount=None):
        if amount is None:
            await ctx.channel.purge(limit=6)
        elif amount == "todas":
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit=int(amount)+1)

    @commands.command(aliases=["retirar"])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason = "Nenhum motivo foi providenciado"):
        await member.send(f"Você foi retirado pelo motivo:\n{reason}")
        await member.kick(reason=reason)

    @commands.command(aliases=["banir"])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason = "Nenhum motivo foi providenciado"):
        await member.send(f"{member.name} foi banido pelo motivo:\n{reason}")
        await member.ban(reason=reason)

    @commands.command()
    @commands.has_role('Admin')
    async def quit(self, ctx):
        await ctx.send("Shutting down the bot.")
        return await self.bot.logout()


def setup(bot):
    bot.add_cog(AdminCog(bot))
