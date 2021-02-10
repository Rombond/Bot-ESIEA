import asyncio
import configparser
from export import *
from tokenClass import *
from discord.ext import commands


config = configparser.ConfigParser()
config.read('config.ini')

bot = commands.Bot(command_prefix=config['DEFAULT']['prefix'])
channelID = int(config['DEFAULT']['channelID'])
channel = bot.get_channel(channelID)
lastMsg = None
minuteLeft = int(config['DEFAULT']['minuteRappel'])
TOKEN = config['DEFAULT']['tok']
users = []
username = config['DEFAULT']['username']
password = config['DEFAULT']['password']


async def getData():
    toke = await Token.post(Token(), username, password)
    dataF = await Export(token=toke).getCalendarDaily()
    return dataF


def recap(data):
    string = "Bonjour à tous, voici un récap des présences de la journée :\n\n"
    for d in data:
        string += ("> - **" + d[0] + "** de **" + d[1] + "** à **" + d[2] + "**\n")
    string += "\nPassez une bonne journée"
    return string


def msgWithRappel(d):
    string = "@here\n\nLa présence du cours : **" + d[0] + "** vient d'ouvrir ici :\n> " + d[3] + "\nElle ferme à **" \
             + d[2] + "**\nMettez un ⏲️ pour avoir un rappel juste avant la fermeture de la présence\n"
    return string


async def reminder(d):
    s = "Tu m'as demandé de te rappeler ta présence, il te reste **" + str(minuteLeft) + "** minutes\n" + d[3]
    for user in users:
        await user.send(s)
    users.clear()


async def checkTime():
    now = datetime.datetime.now()
    data = await getData()
    if not data:
        return
    string = ""
    rappel = False
    if now.hour == 8 and now.minute == 30:
        string = recap(data)
    else:
        for d in data:
            if now.hour == int(d[1].split(':')[0]) and now.minute == int(d[1].split(':')[1]):
                string = msgWithRappel(d)
                rappel = True
            elif now.hour == int(d[2].split(':')[0]) and now.minute+minuteLeft == int(d[2].split(':')[1]):
                if len(users) > 0:
                    await reminder(d)
    if string != "":
        global lastMsg
        lastMsg = await channel.send(string)
        if rappel:
            await lastMsg.add_reaction('⏲')


@bot.event
async def BgTask():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await checkTime()
        await asyncio.sleep(60)


@bot.command(name='recap')
async def sendRecap(ctx):
    data = await getData()
    if not data:
        await channel.send("Il n'y a rien aujourd'hui")
        return
    msg = recap(data)
    await channel.send(msg)


@bot.command(name='first')
async def sendFirst(ctx):
    data = await getData()
    if not data:
        await channel.send("Il n'y a rien aujourd'hui")
        return
    msg = msgWithRappel(data[0])
    msg += "\n**Les rappels ne fonctionnent pas sur la commande**"
    await channel.send(msg)


@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.id != lastMsg.id or user == lastMsg.author:
        return
    if reaction.emoji == '⏲':
        users.append(user)


@bot.event
async def on_ready():
    global channel
    channel = bot.get_channel(channelID)


bot.loop.create_task(BgTask())
bot.run(TOKEN)
