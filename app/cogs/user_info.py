from disnake.ext import commands
from disnake import ApplicationCommandInteraction
from app.utils.registration import require_registration, is_registered
from app.utils.database import SessionLocal

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="user_info", description="Получить информацию о пользователе")
    @require_registration()
    async def user_info(
        self,
        interaction: ApplicationCommandInteraction,
        user_id: str = None # Disnake makes it int32 while id is ACTUALLY🤓 int64. It breaks the command lol
    ):
        async with SessionLocal() as session:
            if user_id is None:
                user_id = interaction.author.id

            try:
                user = await is_registered(int(user_id))
            except ValueError:
                await interaction.response.send_message("can u stop fucking around and give an actual id?", ephemeral=True)
                return
            
            if user:
                await interaction.response.send_message(
                    f"**ID:** {user.discord_id}\n**Имя:** {user.username}\n**Зарегистрирован:** {user.joined_at}"
                )
            else:
                await interaction.response.send_message("Пользователь не найден.", ephemeral=True)

def setup(bot):
    bot.add_cog(UserInfo(bot))
