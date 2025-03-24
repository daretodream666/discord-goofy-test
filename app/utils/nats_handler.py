import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

class NATSHandler:
    def __init__(self, bot, nats_url="nats://localhost:4222"):
        self.bot = bot
        self.nats_url = nats_url
        self.nc = NATS()

    async def connect(self):
        while True:
            try:
                await self.nc.connect(self.nats_url, allow_reconnect=True)
                print("Подключено к NATS!")
                break
            except (ErrConnectionClosed, ErrTimeout, ErrNoServers) as e:
                print(f"Ошибка подключения к NATS: {e}. Повторная попытка...")
                await asyncio.sleep(5)

    async def subscribe_to_broadcast(self):
        async def message_handler(msg):
            try:
                subject = msg.subject
                data = msg.data.decode()
                print(f"Получено сообщение: {data} на тему {subject}")

                if subject.startswith("broadcast."):
                    channel_id = subject.split(".")[1]

                    channel = await self.bot.fetch_channel(channel_id)
                    await channel.send(data)
            except Exception as e:
                print(f"Ошибка обработки сообщения из NATS: {e}")

        await self.nc.subscribe("broadcast.*", cb=message_handler)

    async def publish_message(self, channel_id, message):
        try:
            subject = f"broadcast.{channel_id}"
            await self.nc.publish(subject, message.encode())
            print(f"Сообщение опубликовано в NATS: {subject}")
        except Exception as e:
            print(f"Ошибка публикации сообщения в NATS: {e}")

    async def close(self):
        await self.nc.drain()
