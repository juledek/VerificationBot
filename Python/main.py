import discord
import os
from discord.ext import commands
import VerificationBot
import WarningBot
import aiofiles
import RolesBot

#bot = discord.Client()

bot = commands.Bot(command_prefix="$")
TOKEN = os.environ['TOKEN']
bot.warnings = {} # guild_id : {member_id: [count, [(admin_id, reason)]]}
#badWordList = ['cock', 'deepthroat', 'dick', 'cumshot','fuck', 'sperm', 'jerk off', 'ass', 'tits', 'fingering', 'masturbate', 'bitch', 'blowjob', 'prostitute', 'bullshit', 'dumbass', 'dickhead', 'pussy', 'piss', 'asshole', 'erection', 'foreskin', 'gag', 'handjob', 'licking', 'nude', 'penis', 'porn', 'viagra', 'virgin', 'vagina', 'vulva', 'wet dream', 'threesome', 'orgy', 'bdsm', 'hickey', 'condom', 'sexting', 'squirt', 'testicles', 'anal', 'bareback', 'bukkake', 'creampie', 'stripper', 'strap-on', 'missionary', 'clitoris', 'cock ring', 'fleshlight', 'butt plug', 'moan', 'wank', 'sucking', 'scissoring', 'slut', 'cumming', 'faggot', 'anus']
badWordList = ['abcdcba']
bot.remove_command('help')
logChannelId = 855123222037790730

@bot.event
async def on_ready():
    for guild in bot.guilds:
        bot.warnings[guild.id] = {}
        
        async with aiofiles.open(f"{guild.id}.txt", mode="a") as temp:
            pass

        async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")

                try:
                    bot.warnings[guild.id][member_id][0] += 1
                    bot.warnings[guild.id][member_id][1].append((admin_id, reason))

                except KeyError:
                    bot.warnings[guild.id][member_id] = [1, [(admin_id, reason)]] 
    
    print(bot.user.name + " is ready.")

@bot.event
async def on_guild_join(guild):
    bot.warnings[guild.id] = {}





##Bot 1: Verification, $hey $student $verify $bugs $help VerificationBot

##what did you message me??
@bot.command()
async def hey(ctx):
  await VerificationBot.hey(ctx)

@bot.command()
async def explain(ctx, topic):
  if topic.__eq__('verificatie'):
    await ctx.channel.send(
        'Hallo! Ik ben de IT Bot van de TI server. Ik kan verifieren of je student of medewerker bent bij HOGENT. Om aan het verificatieproces te beginnen kan je in dit kanaal $hey sturen. Als je problemen of bugs tegenkomt, gebruik dan het commando $bugs voor meer uitleg. Hopelijk helpt dit!'
    )

  if topic.__eq__('warnings'):
    await ctx.channel.send('Hallo! Ik ben de IT Bot van de TI server. Ik kan ervoor zorgen dat er warnings worden gestuurd naar bepaalde mensen. Stuur het bericht ')

@bot.command()
async def verify(ctx, token):
  ##check if the given token is the correct token
  await VerificationBot.verify(ctx, bot, token)

@bot.command()
async def student(ctx, email):
  await VerificationBot.sendmail(ctx, email)

  """"
    if message.content.startswith('$bugs'):
      await message.author.send(
			  'Herhaal $bugs in het juiste kanaal in de TI server, daar kan ik je verder helpen!'
			)"""


@bot.command()
async def bugs(ctx):
  print('test')
  myid = '<@&853247302625001482>'
  channel = '<#773873688528289823>'
  return await ctx.send(
      'Ben je een bug of probleem tegengekomen met de bot, laat het ons dan zeker weten in '
      + channel +
      ' of als het echt dringend is kan je een van onze ' + myid +
      ' een privébericht sturen')

  
##Bot 2: Warnings, $warn [MEMBER] [REASON], $Warnings [PERSON]
  ##Also included is a messagereader that autoresponds to messages with words from the bad word list :)

##warns a certain member for a certain reason
@bot.command()
async def warn(ctx, channel: discord.TextChannel=None, member: discord.Member=None, *, reason=None):
  await WarningBot.warn(ctx, bot, channel, member, reason)
        
    
##Gives all the warnings a certain member has had
@bot.command()
async def warnings(ctx, member:discord.Member=None):
  await WarningBot.warnings(ctx, bot, member)

@bot.command()
async def deleteWarning(ctx, member:discord.Member=None, *, reason=None):
  await WarningBot.deleteWarning(ctx, bot, reason, member)

@bot.command()
async def clearWarnings(ctx, member:discord.Member=None):
  await WarningBot.clearWarnings(ctx, bot, member)

@bot.command()
async def help(ctx, bot):
  if(bot.__eq__("WarningBot")):
    await WarningBot.help(ctx)
  if(bot.__eq__("VerificationBot")):
    await VerificationBot.help(ctx)

##BOT 3: ROLES
@bot.command()
async def newRoleMessage(ctx):
  RolesBot.addNewRolesMessage(ctx)

@bot.command(name='numgame')
async def numgame(ctx):

    def check(message):
        print(f"{message.author} {ctx.message.author} {ctx.channel} {message.channel}")
        return message.author.__eq__(ctx.message.author) and message.channel.__eq__(ctx.channel)
  ##Get the chosen channel
    await ctx.send('Hey there! Please send me in which channel you want the message to be in.')
    msg = await bot.wait_for('message', check = check, timeout=30)
    #bot.get_channel(logChannelId)
    chosenChannel = bot.get_channel(int(msg.content.split('#')[1].split('>')[0]))
    print(chosenChannel)

##Get the chosen title and description of a the message.
    await ctx.send('Fantastisch. Stuur nu je titel en beschrijving door van je bericht op de volgende manier: titel | beschrijving')
    msg = await bot.wait_for('message', timeout=30)
    try:
      titDescr = msg.content.split('|')
      chosenTitel = titDescr[0]
      chosenDescription = titDescr[1]
    except IndexError:
      ctx.send("De syntax van jouw bericht klopt niet, probeer het opnieuw vanaf het begin. Dankje.")

##now await the right emojis and roles





    await ctx.send('Super! Geef nu alle rollen die moeten toegevoegd worden aan het bericht. Doe dit op de volgende manier -> Stuur mij de naam van de rol en reageer het juiste emoji op je bericht. Eens je klaar bent stuur done ')
    roles = []
    while not msg.content.__eq__("done"):
      
      msg = await bot.wait_for('message', check = check, timeout=30)

      
      if(msg.content.lower().__eq__("done")):
        break

      try:
        reaction, user = await bot.wait_for('reaction_add', timeout=15.0)
        print(reaction)
      except:
        await ctx.send('👎')

      
      else:
        roleMessage = []
        roleMessage.append(reaction)
        roleMessage.append(msg.content)
        roles.append(roleMessage)
      print(roles)

    print('out of while')

    embed = discord.Embed(title = chosenTitel, description = chosenDescription, colour = discord.Colour.green())

    message = await chosenChannel.send(embed = embed)
    ##save everything
    for word in roles:
      (reaction, role) = (word)
      await message.add_reaction(reaction)
      async with aiofiles.open(f"{message.id}.txt", mode="a") as file:
          await file.write(f"{reaction.emoji} {role}")


@bot.event
async def on_reaction_add(reaction, user):
  roleAdded = False
  if bot != user:
    if os.path.isfile(f'{reaction.message.id}.txt'):

      try:
        async with aiofiles.open(f"{reaction.message.id}.txt", mode="r") as file:
          lines = await file.readlines()
          
          for line in lines:
            print(lines)
            (firstWord, rest) = line.split(maxsplit=1)
            if reaction.emoji in line:
              print(rest)
              role = discord.utils.get(reaction.message.guild.roles, name=rest)
              print(role)
              await user.add_roles(role)
              roleAdded = True
          
          if roleAdded:
            logEmbed = discord.Embed(title = "Role added", description= f"{user} had a role added.\n Role {role}\n", colour = discord.Colour.green())
            await bot.get_channel(logChannelId).send(embed = logEmbed)

      except FileNotFoundError:
        print(FileNotFoundError)
        
    else:
      print("Message isnt in reactionfile")



##AUTOWARNINGS
@bot.event
async def on_message(message):
    if message.author == bot:
        return
    else:
      try:
        wordsInMessage = message.content.lower().split(' ')
        print(message.content)
        for messageWord in wordsInMessage:
          for word in badWordList:
            if word.__eq__(messageWord):
              print(word)
              print(messageWord)
              await message.reply(f'{message.author.mention}, je hebt een woord gebruikt van de Bad Word List. Het is niet toegestaan om dit woord te gebruiken, daarom krijg je een warning. Denk je dat dit bericht een bug is, type $bugs.')
              await WarningBot.warn(message, bot, message.channel, message.author, "Taalgebruik")
      except KeyError:
        await message.channel.send()
      await bot.process_commands(message)

@warn.error
async def clear_error(ctx, error):
    await ctx.channel.send("Oeps! Er liep iets mis. Heb je het bericht juist gestuurd? $warn [CHANNEL] [MEMBER] [REASON]")

@deleteWarning.error
async def delW_error(ctx, error):
    await ctx.channel.send("Oeps! Er liep iets mis. Heb je het bericht juist gestuurd? $deleteWarning [MEMBER] [REASON]")


bot.run(TOKEN)
