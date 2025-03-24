import grpc
from . import service_pb2
from . import service_pb2_grpc
import disnake
from disnake.ext import commands

class BotService(service_pb2_grpc.BotServiceServicer):
    def __init__(self, bot):
        self.bot = bot

    async def SendMessage(self, request, context):
        try:
            channel = await self.bot.fetch_channel(request.channel_id)
            if not isinstance(channel, (disnake.TextChannel, disnake.Thread)):
                return service_pb2.SendMessageResponse(
                    status="Ошибка", 
                    error="Указанный канал не поддерживает отправку сообщений."
                )

            if not request.message.strip():
                return service_pb2.SendMessageResponse(
                    status="Ошибка", 
                    error="Сообщение не может быть пустым."
                )

            await channel.send(request.message)
            return service_pb2.SendMessageResponse(
                status="Успех", 
                error=""
            )
        except disnake.Forbidden:
            return service_pb2.SendMessageResponse(
                status="Ошибка", 
                error="Бот не имеет прав для отправки сообщений в этот канал."
            )
        except disnake.NotFound:
            return service_pb2.SendMessageResponse(
                status="Ошибка", 
                error="Канал с указанным ID не найден."
            )
        except Exception as e:
            return service_pb2.SendMessageResponse(
                status="Ошибка", 
                error=f"Произошла ошибка: {str(e)}"
            )

async def serve(bot):
    server = grpc.aio.server()
    service_pb2_grpc.add_BotServiceServicer_to_server(BotService(bot), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC сервер запущен на порту 50051")
    await server.start()
    await server.wait_for_termination()

