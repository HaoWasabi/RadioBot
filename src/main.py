import os, logging, tracemalloc, asyncio, nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from bll.channel_bll import ChannelBLL
from bll.group_bll import GroupBLL
from bll.server_bll import ServerBLL

# Load environment variables
load_dotenv()
# Start memory tracking
tracemalloc.start()

# Set up intents
intents = nextcord.Intents.default()
intents.message_content = True
intents.guilds = True

# Set up logging
logger = logging.getLogger(__name__)

# Set up bot instance
bot = commands.Bot(command_prefix='_', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} đã sẵn sàng!")


# Load cogs asynchronously
async def load_cogs():
    cogs_dir = os.path.join(os.path.dirname(__file__), 'cogs')
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            cog_name = f'cogs.{filename[:-3]}'
            try:
                bot.load_extension(cog_name)
                logger.info(f'Successfully loaded extension {cog_name}')
            except Exception as e:
                logger.error(f'Failed to load extension {cog_name}: {e}')
                
# Create database
def create_database():
    GroupBLL()
    ChannelBLL()
    ServerBLL()

def run_bot():
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN:
        logger.info(f"Token found: {TOKEN[:5]}...")  # Log 5 ký tự đầu để kiểm tra token
        bot.run(TOKEN)
    else:
        logger.error("DISCORD_TOKEN not found in .env file.")

if __name__ == "__main__":   
    # Create database 
    create_database()
    
    # ## Run bot and load cogs
    asyncio.run(load_cogs())
    run_bot()