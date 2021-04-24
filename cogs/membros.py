import os
import datetime
import discord
from discord.ext import commands

class MembroCog(commands.Cog, name = "Membros"):
    """Comandos disponíveis para todos membros do servidor."""

    def __init__(self, bot):
        self.bot = bot

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

    @commands.command()
    async def registrar(self, ctx):
        link = "https://www.sympla.com.br/campeonato-quick-play-free-fire__1184130"
        await ctx.send(f"Faça sua inscrição no campeonato FREE FIRE do QUICK PLAY (ABRIL 2021) no link abaixo!\n{link}")
        #await ctx.send("Aguarde a definição do próximo campeonato...")

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
        print(regras_txt)
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
    bot.add_cog(MembroCog(bot))
