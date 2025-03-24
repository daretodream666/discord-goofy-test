import disnake
from disnake.ext import commands

from app.utils.registration import require_registration


class SetStatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Set status for bot")
    @require_registration()
    async def set_status(self, interaction: disnake.ApplicationCommandInteraction,
                        activity_type: str = commands.Param(choices=['Playing', 'Listening', 'Watching']), 
                        status: str = commands.Param(description="Enter bot activity")):
        match activity_type:
            case "Playing":
                activity = disnake.Game(name=status)
            case "Listening":
                activity = disnake.Activity(type=disnake.ActivityType.listening, name=status)
            case "Watching":
                activity = disnake.Activity(type=disnake.ActivityType.watching, name=status)
        await self.bot.change_presence(activity=activity)
        await interaction.response.send_message("ok done", ephemeral=True)

def setup(bot):
    bot.add_cog(SetStatusCog(bot))