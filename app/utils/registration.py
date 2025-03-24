from functools import wraps
from sqlalchemy.future import select
from app.utils.database import SessionLocal, BotUser
from disnake.ext import commands

async def is_registered(user_id):
    async with SessionLocal() as session:
        result = await session.execute(select(BotUser).where(BotUser.discord_id == user_id))
        user = result.scalars().first()
        return user

def require_registration():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs): # Messy stuff, had some issues with args
            if args and isinstance(args[0], commands.Cog):
                interaction = args[1]
            elif args:
                interaction = args[0]
            elif 'interaction' in kwargs:
                interaction = kwargs['interaction']
            else:
                raise RuntimeError("No arguments passed to the command")

            if await is_registered(interaction.author.id):
                return await func(*args, **kwargs)
            await interaction.response.send_message("Ты не зарегистрирован! Введи `/register` для регистрации.")
        return wrapper
    return decorator
