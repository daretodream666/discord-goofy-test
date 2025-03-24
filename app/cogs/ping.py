import disnake
from disnake.ext import commands

from app.utils.registration import require_registration

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Play ping pong")
    @require_registration()
    async def ping(self, interaction: disnake.ApplicationCommandInteraction):
        latency = self.bot.latency * 1000
        await interaction.response.send_message(f"Pong took {latency:.2f} ms", ephemeral=True)

def setup(bot):
    bot.add_cog(PingCog(bot))