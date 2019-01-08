import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import os
import mtranslate as mt
import emoji as emojimodule
import random

prefix = '~'

Client = discord.Client()
client = commands.Bot(command_prefix=prefix)

OWNER_ROLE = '500647537116708885'

languages = {
':United_Kingdom:':'gb',
':United_States:':'gb',
':Canada:':'gb',
':Argentina:':'es',
':Bolivia:':'es',
':Chile:':'es',
':Colombia:':'es',
':Cuba:':'es',
':Dominican_Republic:':'es',
':Ecuador:':'es',
':El_Salvador:':'es',
':Equatorial_Guinea:':'es',
':Guatemala:':'es',
':Honduras:':'es',
':Mexico:':'es',
':Nicaragua:':'es',
':Panama:':'es',
':Paraguay:':'es',
':Peru:':'es',
':Spain:':'es',
':Uruguay:':'es',
':Venezuela:':'es',
':Germany:':'de',
':Norway:':'no',
':Russia:':'ru',
':France:':'fr',
':Germany:':'de',
':Portugal:':'pt',
':Polish:':'pl',
':Ceuta_&_Melilla:':'es'
}

#---APP---

@client.event
async def on_ready():
    print('Bot Loaded')
    await client.change_presence(game=discord.Game(name='Type ~commands for help'))

@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    content = reaction.message.content
    emoji = reaction.emoji

    name = emojimodule.demojize(emoji)
    embed = discord.Embed(colour=0xff8000)

    if name in languages:
        language = languages[name]
        msg = mt.translate(content, language, 'auto')
        embed.add_field(name=content, value=msg, inline=False)
        await client.send_message(channel, embed=embed)

    await client.send_message(channel, '{} has added {} to the the message {}'.format(user.name, reaction.emoji, reaction.message.content))

@client.command(pass_context=True)
async def commands(ctx):
    author = ctx.message.author
    embed = discord.Embed(colour=0xff8000)

    msg = '''```-React with a flag to get translations
~translations = Gets the flags that you can react with
~translate <target_language> [message...]
~translate_message <target_language> <message_id>
~clear <number of messages to purge, 5 is the default>```'''

    await client.send_message(ctx.message.channel, content=msg)

@client.command(pass_context=True)
async def translate(ctx, target_language='', *message):
    if not target_language or not message:
        await client.send_message(ctx.message.channel, content='```~translate <target_language> <message_id OR message...>```')
    else:
        try:
            #find messages
            id = message[0]

            msg = await client.get_message(ctx.message.channel, id)
            trans = mt.translate(msg.content, target_language, 'auto')

            embed = discord.Embed(colour=0xff8000)
            embed.add_field(name='Translation: '+trans, value='Original: '+msg.content, inline=False)

            await client.send_message(ctx.message.channel, embed=embed)
        except Exception:
            #translate raw message
            msg = mt.translate(' '.join(message), target_language, 'auto')
            await client.send_message(ctx.message.channel, content=msg)

@client.command(pass_context=True)
async def translate_message(ctx, target_language='', message_id=''):
    if not target_language or not message_id:
        await client.send_message(ctx.message.channel, content='```~translate_message <target_language> <message_id>```')
    else:
        msg = await client.get_message(ctx.message.channel, message_id)
        trans = mt.translate(msg.content, target_language, 'auto')

        embed = discord.Embed(colour=0xff8000)
        embed.add_field(name='Translation: '+trans, value='Original: '+msg.content, inline=False)

        await client.send_message(ctx.message.channel, embed=embed)

@client.command(pass_context=True)
async def clear(ctx, amount='5'):
    channel = ctx.message.channel
    author = ctx.message.author

    if OWNER_ROLE in [y.id for y in author.roles]:
        if float(amount).is_integer():
            messages = []
            async for msg in client.logs_from(channel, limit=int(amount)+1):
                messages.append(msg)
            await client.delete_messages(messages)
        else:
            await client.say('Use an integer')
    else:
        msg = "Hey <@{}>, you aren't alpha male enough to do that :smaller:".format(author.id)
        await client.send_message(channel, msg)

client.run(os.environ.get('TOKEN'))
