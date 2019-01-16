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
client.remove_command('help')

OWNER_ROLE = '500647537116708885'
ADAM_PING = '<@!394978551985602571>'
QOTD_BOT_CHANNEL = '533373064537440267'
QOTD_CHANNEL = '531461072540925982'

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

#---Functions---
def get_question_string(message):
    language, question, author = message.content.split("\x11")

    translations = []
    for lang in ['en', 'es', 'fr', 'de', 'ja', 'ko', 'cs', 'ru', 'sv']:
        if lang == language:
            translations.append(question)
        else:
            translations.append(mt.translate(question, to_language=lang, from_language=language))
    translations.append(author)

    string = '''--------------------
:flag_gb: {}
:flag_es: {}
:flag_fr: {}
:flag_de: {}
:flag_jp: {}
:flag_kr: {}
:flag_cz: {}
:flag_ru: {}
:flag_se: {}

The question of the day was submitted by - <@{}>. If any translations are wrong, feel free to tell a member of the staff team :smiley:
--------------------'''.format(*translations)

    return string

    #need to add translations to the question

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

    #await client.send_message(channel, '{} has added {} to the the message {}'.format(user.name, reaction.emoji, reaction.message.content))

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(colour=0xff8000)

    msg = '''```-React with a flag to get translations (if you want more flags adding, please ping Adam C)

~language_codes = Gets all the codes for languages that are used for ~translate and ~qotd

~translate <target_language> [message...]

~translate <target_language> <message_id>

~qotd <current_language> [question...]

~clear <number of messages to purge, 5 is the default>```'''

    await client.send_message(ctx.message.channel, content=msg)

@client.command(pass_context=True)
async def language_codes(ctx):
    await client.send_message(ctx.message.channel, content='''----*Language Codes*----
:flag_gb: = en
:flag_es: = es
:flag_fr: = fr
:flag_de: = de
:flag_jp: = ja
:flag_kr: = ko
:flag_cz: = cs
:flag_ru: = ru
:flag_se: = sv
''')

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
async def qotd(ctx, language='', *question):
    if not language or not question:
        await client.send_message(ctx.message.channel, content='```~qotd <current_language> [question...]```')
    else:
        author = ctx.message.author
        question = ' '.join(question)

        messages = [[ctx.message.channel, 'Thanks {} :P'.format(author.mention)], [client.get_channel(QOTD_BOT_CHANNEL), "{}\x11{}\x11{}".format(language, question, author.id)]]
        for message in messages:
            await client.send_message(message[0], content=message[1])

@client.command(pass_context=True)
async def next_qotd(ctx):
    if OWNER_ROLE in [y.id for y in ctx.message.author.roles]:
        questions = []
        async for q in client.logs_from(client.get_channel(QOTD_BOT_CHANNEL)):
            questions.append(q)
        questions.reverse()
        question = questions[0]

        for command in [client.delete_message(question), client.send_message(client.get_channel(QOTD_CHANNEL), content=get_question_string(question))]:
            await command
    else:
        await client.send_message(ctx.message.channel, content="Hey <@{}>, you don't have sufficient permission to do this! :smaller:".format(ctx.message.author.id))

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
        await client.send_message(channel, "Hey <@{}>, you don't have sufficient permission to do this! :smaller:".format(author.id))

client.run(os.environ.get('TOKEN'))
