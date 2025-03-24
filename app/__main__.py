import asyncio
from app.bot import bot, run_bot
from grpc1.grpc_server import serve
from app.utils.nats_handler import NATSHandler
from app.utils.database import init_db
import os

TOKEN = os.environ.get('TOKEN')
NATS_URL = os.environ.get('NATS_URL')

async def main():
    nats_handler = NATSHandler(bot, nats_url=NATS_URL)
    
    await asyncio.gather(
        run_bot(TOKEN, nats_handler),           
        nats_handler.connect(),                 
        nats_handler.subscribe_to_broadcast(),  
        serve(bot),                             
        init_db()                               
    )

if __name__ == "__main__":
    loop = asyncio.new_event_loop()  
    asyncio.set_event_loop(loop)     
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
