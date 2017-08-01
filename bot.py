import discord, logging, asyncio
from asyncio.coroutines import *
from app import settings as cfg, commands
print('[!] Import successful.')

"""
This file is the core of the bot.
It handles basic mapping of commands to their literal definitions in "commands.py".
"""

### DISCORD_LOGGING ###
if cfg.DISCORD_LOGGING:
    print('[DISCORD_LOGGING] Starting logger...')
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    print('[DISCORD_LOGGING] Logger started.')
### BOT INIT ###
print('[!] Starting bot. Takes about 5 seconds...')
bot = discord.Client()

@bot.event
async def on_ready():
    print('[+] Logged in as %s\n[+] With ID: %s' %(bot.user.name,bot.user.id))

### HANDLE BOT COMMANDS ###
@bot.event
async def on_message(message):
    if message.author == bot.user:
        if message.content.startswith(cfg.prefix):
            # let's say we had a command: ;ping -v www.google.com
            call = message.content[1::1].split()[0] # command name                  ("ping")
            carg = message.content[1::1].split()[1::1] # seperate arguments         ("-v", "www.google.com")
            marg = message.content[len(call)+2::1] # arguments as whole message     ("-v www.google.com")

            await bot.delete_message(message)

            if call == 'help': # request help info
                if len(carg) > 0:
                    await commands._help(bot, message, carg[0])
                else:
                    await commands._help(bot, message)
            elif call == 'about': # request about info
                await commands.about(bot, message)
            elif call == 'e': # embed a message
                await commands.embed(bot, message, marg)
            elif call == 'ec': # set embed colour
                await commands.embedsetcolor(bot, message, carg)
            elif call == 'ping': # ping a hostname                                  (ah, this is the correct call)
                if len(carg) > 0:
                    await commands.ping(bot, message, carg) #                       (we send our arguments to that command (in commands.py) and it pings)
                else:
                    await commands.ping(bot, message) #                             (we can do a default ping, but the above is what it fits)                               
            elif call == 'sh': # execute and embed a shell script's output
                await commands.executeshell(bot, message, marg)
            elif call == 'eval' or call == 'ev':
                await commands.doeval(bot, message, marg)

            else: # we don't know what they mean in their command
                pass # TODO: add usage
            return
### START BOT ###
try:
    bot.run(cfg.login[0], cfg.login[1]) # the email and password are from "settings.py"
except:
    print('[!] Unable to connect to Discord. Ensure login information is correct, ' /
          'and you are connected to the internet.')
    exit(1)
