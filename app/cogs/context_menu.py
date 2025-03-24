from disnake.ext import commands
from disnake import UserCommandInteraction
from app.utils.registration import is_registered, require_registration
from app.utils.database import SessionLocal, BotUser

class ContextMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.user_command(name="Получить информацию") 
    @require_registration()
    async def get_user_info(self, interaction: UserCommandInteraction, user : int):
        if not await is_registered(user.id):
            await interaction.response.send_message("Этот пользователь не зарегистрирован!", ephemeral=True)
            return

        else:
            await interaction.response.send_message(
                f"**ID:** {user.discord_id}\n"
                f"**Имя:** {user.username}\n"
                f"**Зарегистрирован:** {user.joined_at}"
            )

def setup(bot):
    bot.add_cog(ContextMenu(bot))
