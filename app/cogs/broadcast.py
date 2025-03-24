import disnake
from disnake.ext import commands
from app.utils.registration import require_registration

class BroadcastCog(commands.Cog):
    def __init__(self, bot, nats_handler):
        self.bot = bot
        self.nats_handler = nats_handler

    @commands.slash_command(description="Отправить сообщение через NATS")
    @require_registration()
    async def broadcast(self, interaction: disnake.ApplicationCommandInteraction, channel_id: str, message: str):
        if not message.strip():
            await interaction.response.send_message("Сообщение не может быть пустым.", ephemeral=True)
            return

        try:
            await self.nats_handler.publish_message(channel_id, message)
            await interaction.response.send_message(f"Сообщение опубликовано в тему broadcast.{channel_id}")
        except Exception as e:
            await interaction.response.send_message(f"Ошибка отправки сообщения: {e}", ephemeral=True)

def setup_broadcast(bot,nats_handler):
    bot.add_cog(BroadcastCog(bot, nats_handler))
