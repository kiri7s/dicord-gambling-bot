# main.py

from discord import Intents, Client, Message
from dotenv import load_dotenv
import os
from responses import get_response

# Load environment variables (your Discord token)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up Discord client
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

# Event handler for when the bot is ready
@client.event
async def on_ready():
    print(f'{client.user} is now running!')

# Event handler for incoming messages
@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    username = str(message.author)  # Extract username from message.author
    user_message = message.content


    print(f'[{message.channel}] {username}: "{user_message}"')

    # Call the get_response function from responses.py
    response = get_response(user_message, username)

    # Send the response back
    await message.channel.send(response)

# Run the bot
client.run(token=TOKEN)