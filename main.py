#basic imports
#helpfssdfgsdfsf
import os
import discord
import random
from discord import app_commands
#from discord.ext.commands import Bot
#keep bot up and running
from keep_alive import keep_alive
#for games
import games #currently useless
import dictFuncs
#keep track of time(?)
from datetime import datetime
#from dateutil import tz
#from discord.ext import commands, tasks

#intents = discord.Intents(messages=True, guilds=True)
#GLOBAL VARIABLES
intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
guildID = 764395062153969675
#brain zone: 1021925165912838234
#muppets: 764395062153969675
#time variables
today = datetime.now()
weekday = today.weekday()
time = today.time().replace(microsecond=0)
midnight = datetime.strptime(
  "08:25:00", "%H:%M:%S").time() #convert to a datetime data type

keep_alive()
# secrets ;^)
TOKEN = os.environ['TOKEN']
SERVER = os.environ['MUPPETS']  #this bot is just for vibes, change server manually here (MYSERVER for brain zone, MUPPETS for muppets)


@client.event
async def on_ready():
  for guild in client.guilds:
    if guild.name == SERVER:
      break
  print
  (f'{client.user} is connected to the following guild:\n'
   f'{guild.name}(id: {guild.id})')
  members = '\n - '.join([member.name for member in guild.members])
  print(f'Members:\n - {members}')  #print list of members in the console
  await tree.sync(guild=discord.Object(guildID))

#COMMANDS

@tree.command(name="test", description="test commands", guild=discord.Object(id=guildID))  #can remove guild id but commands will be slower (?)
async def first_command(interaction):
  await interaction.response.send_message("Commands work! :^D")

#GAMES

#turn csv into key-valule pairs
blockDict = dictFuncs.inputWords(open("tblock.csv"))

#split pairs into lists
blockList = list(blockDict.keys())
nameList = list(blockDict.values())

@tree.command(name="bgame", description="minecraft block guessing game :^D", guild=discord.Object(id=guildID))
async def block_game(interaction):
  randomBlock = random.randint(1, len(blockList)) #assumes both lists are the same length
  #await interaction.response.send_message("Guess that block!")
  await interaction.response.send_message(blockList[randomBlock]) 
  # + " " + nameList[randomBlock]

#MESSAGE RESPONSES

@client.event
async def on_message(message):

  #VARIABLES
  wooshNum = random.randint(1, 6)
  screamNum = random.randint(1, 500)
  coolness = [
    "im cool", "i'm cool", "i'm so cool", "im so cool", "i am cool",
    "i am so cool"
  ]
  reactEmote = [
    '<:goodsim:878136216300707900>', '<:badsim:878135979247030283>'
  ]
  reactChance = random.randint(1, 200)

  #prevent botbert recursively responding to himself
  print("message-->", message)
  if message.author == client.user:
    return

#TEXT RESPONSES
#message.content = message.content.lower()
#if message.content.startswith('hey'):
#await message.channel.send('Hello :^)')
#just kinda boring ^ maybe do something else with it

#he can tell you're talking about him
  message.content = message.content.lower()
  if 'botbert can' in message.content:
    await message.channel.send('On it boss :saluting_face:')
  elif 'botbert' in message.content:
    await message.channel.send('That is me hello :^)')

#responses to froggo (rip)
  if message.content == "f is for friends who do stuff together <3":
    await message.channel.send("u is for you and me <3")

  if message.content == "n is for anywhere and anytime at all":
    await message.channel.send("down here in the deep blue sea :^)")

  if message.content == "f is for fire that burns down the whole town":
    await message.channel.send("u is for uranium... ***bombs***")

#response to haikubot
  if message.author.name == "HaikuBot":
    await message.channel.send(
      "hello haikubot\nthank you for your cool poems\nI like them a lot :^)"
    )

#yelling
  if message.content == "b!a" or "aaa" in message.content.lower() and "y" not in message.content.lower():
    scream = ""
    capDecider = random.randrange(3)  #decide scream case

    #loud scream
    if capDecider == 1:
      for i in range(screamNum):
        scream += "A"

  #quiet(er) scream
    elif capDecider == 2:
      for i in range(screamNum):
        scream += "a"

  #fluctuating scream
    else:
      for i in range(screamNum):
        #randomize capitalization
        if random.randrange(2) == 1:
          letter = "A"
        else:
          letter = "a"
        scream += letter

    #print scream string once finished constructing
    await message.channel.send(scream)

#no one in this server is cool
  for cool in coolness:
    if cool in message.content.lower():
      await message.channel.send("no you're not")

  if message.author.name == "koof":
    if "cool" in message.content.lower():
      if "not" not in message.content.lower():
        await message.channel.send("you're not cool")
        await message.add_reaction('<:badsim:878135979247030283>')

#BAN PEOPLE >:^}
#ban yourself
  if message.content == "ban me":
    member = message.author  #the person who sent the message
    banRole = discord.utils.get(member.guild.roles, name="BANNED")
    await member.add_roles(banRole)
    await message.channel.send("kinda weird but ok")

  #ban everyone
  if message.content == "ban everyone":
    #loop through all the members in the server
    for member in message.guild.members:
      #don't ban them if theyre a bot because it would be a pain to unban them all
      botRole = discord.utils.get(member.guild.roles, name="bot")
      if botRole not in member.roles:
        #give everyone else the banned role hehe
        banRole = discord.utils.get(member.guild.roles, name="BANNED")
        await member.add_roles(banRole)
    await message.channel.send("done. none of you are free of sin")
    await message.channel.send(
      "https://i.kym-cdn.com/photos/images/newsfeed/001/242/769/89d.gif"
    )  #too much? funny for now, maybe just pick the message or text

  #targetted banning (AHA IT WORKS >:D)
  if "ban" in message.content.lower() and "banned" not in message.content.lower():
    for member in message.guild.members:
      if member in message.mentions:
        await message.channel.send("haha get banned " + member.nick)
        banRole = discord.utils.get(member.guild.roles, name="BANNED")
        await member.add_roles(banRole)

  #banned words
  if "bread" in message.content.lower():
    if message.channel.id != 1108636403786600468:
      await message.delete()
      await message.channel.send("*you cannot speak of bread outside of the bread channel*")
      member = message.author  #the person who sent the message
      banRole = discord.utils.get(member.guild.roles, name="BANNED")
      await member.add_roles(banRole)
      await message.channel.send("***banned***")
      
  #nickname changes
  #if "change name" in message.content.lower():
    #for member in message.guild.members:
      #if member in message.mentions:
        #await member.edit(nick="message.content")
#does not have the permissions for this and I am too lazy to find how to change them
  
#randomized chance to react to messages expressing approval or disapproval
  if (reactChance == 1):  #1 is arbitrary, just lets me change the chance more easily
    await message.add_reaction(reactEmote[random.randint(0,len(reactEmote) - 1)])  #randomly choose an emote from the list to react with

#SEND IMAGES/GIFS
#good luck woosh :)
  if message.content.lower() == "woosh" or message.content == "https://tenor.com/view/magikaikai-magicat-magic-cat-magikai-gif-20378023":
    for i in range(wooshNum):
      await message.channel.send(
        "https://tenor.com/view/magikaikai-magicat-magic-cat-magikai-gif-20378023"
      )

#no u
  if message.content.lower() == "no u" or message.content.lower() == "no you":
    if random.randint(1, 2) == 1:
      await message.channel.send(
        "https://tenor.com/view/reverse-nozumi-uno-jojo-card-gif-21302313")
    else:
      await message.channel.send(
        "https://tenor.com/view/yugioh-no-u-no-you-reverse-uno-uno-gif-22508660"
      )

#lets goooo
  if "lets go" in message.content.lower() or "letsgo" in message.content.lower(
  ):
    if random.randint(1, 20) == 1:
      await message.channel.send(
        "https://cdn.discordapp.com/attachments/1022022584184881172/1048908946666164274/lets-go-lets-goo.png"
      )

#boomer
  if "boomer" in message.content.lower():
    if random.randint(1,30) == 1:
      await message.channel.send("https://cdn.discordapp.com/attachments/1108641500922904677/1122068724472619028/doooooomer.png")
    else:
      await message.channel.send("https://dodo.ac/np/images/7/7d/Boomer_NH.png")

#jon crying
  if "arbuckle" in message.content.lower():
    await message.delete()
    await message.channel.send(
      "https://cdn.discordapp.com/attachments/1021925166441308162/1076270818369216582/IMG_3827.png"
    )

#pinecone
  if "invite" in message.content.lower():
    await message.channel.send(
      "https://cdn.discordapp.com/attachments/764836726690414602/1086125728770310294/image.png"
    )

#SEND VIDEOS
#every second you're not running I'm only getting closer
  if message.content.lower() == "run":
    await message.channel.send("https://www.youtube.com/shorts/uoLymUpqZt4")

#TIME BASED
#just a test 4 saturday shorts

  if message.content == "test":
    await message.channel.send(time)
    await message.channel.send(midnight)
    await message.channel.send(weekday)

    if time == midnight:
      await message.channel.send("matched if works")
    else:
      await message.channel.send("not matched works")
    if weekday == 7:
      await message.channel.send("second if works")

    choseChannel = client.get_channel(
      1044920307003170826)  #'botbert's bedroom' in brain
    await choseChannel.send("channel and message work")

  #all the individual bits work but it doesnt always check the time and looping it forever makes other parts of the bot stop working

  if weekday == 5:  # saturday is 5 not 6 for some reason
    if time == midnight:  #at midnight check the date
      #channel = client.get_channel(953216042728030258) #'wednesday' in muppets
      choseChannel = client.get_channel(
        1044920307003170826)  #'botbert's bedroom' in brain
      await choseChannel.send("https://youtu.be/Xud0YWhQsXc")
      #so the issue with this is that it's only checking every time someone sends a message because its in the on_message event - move it out?

  if "saturday" in message.content:
    if weekday == 5:
      await message.channel.send("https://youtu.be/Xud0YWhQsXc")
      #for now anyway
  #await bot.process_commands(message)
  #client.process_commands(message)


#If a new member joins the server dm them and tell them to leave (probably never gonna be used tbh)
@client.event
async def on_member_join(member):
  await member.create_dm()  #dms the member
  await member.dm_channel.send(
    f'Who are you. Get out of my server {member.name}')


#I don't want to create a new account to test this. I'm just gonna assume it works (it doesnt :( )

#RUN
client.run(TOKEN)
