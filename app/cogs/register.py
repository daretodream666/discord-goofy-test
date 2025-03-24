from disnake.ext import commands
from disnake import ApplicationCommandInteraction
from app.utils.database import SessionLocal, BotUser
from app.utils.registration import is_registered

class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="register", description="Зарегистрироваться в боте")
    async def register(self, interaction: ApplicationCommandInteraction):
        async with SessionLocal() as session:
            if is_registered:
                await interaction.response.send_message("Ты уже зарегистрирован!", ephemeral=True)
                return
            
            new_user = BotUser(
                discord_id=interaction.author.id,
                username=interaction.author.name
            )
            session.add(new_user)
            await session.commit()

            await interaction.response.send_message(f"{interaction.author.mention}, ты зарегистрирован!")

def setup(bot):
    bot.add_cog(Register(bot))
