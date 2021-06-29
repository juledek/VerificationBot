import discord
import os
from discord.ext import commands
import smtplib
import time
from email.mime.text import MIMEText
from uuid import uuid4
from replit import db

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents)
    
logChannelId = 855123222037790730
StudentEmails = 'student.hogent.be'
LectorEmails = 'hogent.be'

async def hey(ctx):
	botmessage = await ctx.send(
	    'Ik heb je een privé bericht gestuurd om je te verifiëren.')
	await ctx.message.delete()
	await ctx.author.send(
	    'Hallo daar! Ik ben de verificatie bot van de TI server. Ik kan verifieren of je student bent aan HOGENT. Dit gebeurt in stappen;\n\nJij stuurt naar mij jouw HOGENT email adres door zodat ik daar jouw unieke token naartoe kan sturen.\nEens je de email ontvangen hebt kan je het naar mij terugsturen zodat ik weet dat jij degene bent die de mail ontvangen heeft. Op die manier kan ik verifiëren of je een student of medewerker bent! \n\n'
	)
	await ctx.author.send(
	    "Hiervoor hebben we jouw school email nodig. Daarvoor moet je mij volgend bericht sturen: $student youremail@school.be"
	)
	time.sleep(5)
	await botmessage.delete()

##@bot.command()
async def verify(ctx, bot, token):
  possibleToken = token
  student = ctx.author.name
  tokenName = student + '_Token'
  print(tokenName)
  try:
    Token = db[tokenName]
    if (possibleToken == Token):
      member = ctx.author
      role = discord.utils.find(lambda r: r.name == 'Verified', ctx.guild.roles)
      if role is not None:
			##role = discord.utils.get(message.guild.roles, name="Verified")
        await member.add_roles(role)
        botmessage = await ctx.send('Je bent geverifieerd als student! Check jouw rollen!')
        del db[tokenName]
        logEmbed = discord.Embed(title = "Verification", description= f"{member} has been verified with token {possibleToken}", colour = discord.Colour.blue())
        await bot.get_channel(logChannelId).send(embed = logEmbed)
      else:
        ctx.send(
			    'Oeps! Er liep iets mis. Het ziet er naar uit dat er geen Verified rol is in deze server. Voeg eerst de rol Verified toe aan de server.'
			  )

    else:
      botmessage = await ctx.send('Oeps! Er liep iets mis. Heb je de verkeerde Token gekopieerd?')
  except KeyError:
    botmessage = await ctx.send('Oeps! Er liep iets mis. Heb je de verkeerde Token gekopieerd?')
	
  await ctx.message.delete()
  time.sleep(5)
  await botmessage.delete()
  ##log
  


async def sendmail(ctx, email):
	##get the email school type
  schoolType = email.split('@')[1]
  schoolType = schoolType.lower()

	##If the email is any other email than the accepted school emails
  if schoolType == StudentEmails:
		##Get email
	  sender = 'tidiscordserver@gmail.com'
	  Email = email

		##build email
	  receiver = Email
	  bodySend = await buildBody(ctx.author.name)
	  msg = MIMEText(bodySend)
	  msg['Subject'] = 'Student verificatie'
	  msg['From'] = sender
	  msg['To'] = receiver
	  msg['Content-Type'] = 'text/plain'

		##sendmail
	  s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
	  s.login(user=sender, password=os.getenv('GMAILPASS'))
	  s.sendmail(sender, receiver, msg.as_string())
	  s.quit()
	  await ctx.author.send(
		    'Ik heb je een mailtje gestuurd. Vergeet niet om je spam folder te bekijken!'
		)
  elif schoolType == LectorEmails:
    sender = 'tidiscordserver@gmail.com'
    Email = email

    ##build email
    receiver = Email
    bodySend = await buildLectorBody(ctx.author.name)
    msg = MIMEText(bodySend)
    msg['Subject'] = 'Student verification'
    msg['From'] = sender
    msg['To'] = receiver
    msg['Content-Type'] = 'text/plain'

    ##sendmail
    s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
    s.login(user=sender, password=os.getenv('GMAILPASS'))
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()
    await ctx.author.send(
        'Ik heb je een mailtje gestuurd. Vergeet niet om je spam folder te bekijken!'
    )
  else:
    await ctx.author.send(
        'Dit is geen HOGENT school email. Kijk alstublieft na dat je mij uw HOGENT email hebt gestuurd.'
    )


async def createToken(user):
##create unique token to verify
  studentToken = uuid4()
  keyName = user + '_Token'
  db[keyName] = studentToken.__str__()
  return studentToken


async def createLectorToken(user):
  lectorToken = uuid4() + 'l'
  keyName = user + '_Token'
  db[keyName] = lectorToken.__str__()
  return lectorToken


async def buildLectorBody(user):
  Token = await createLectorToken(user)
  body = """Hallo daar! \n\nWe zijn zeer blij om te horen dat je aan het proberen bent om te verifiëren dat je een medewerker bij HOGENT bent. Om de verificatie te volbrengen, moet je het token kopieren en terugsturen naar de bot in het juiste kanaal.\n\n\tToken: """ + Token.__str__(
  ) + """\n\nStuur nu een bericht op de volgende manier in het juist kanaal in de TI server (niet in de privé chat);\n\n\t$verify [TOKEN] \n\nZorg ervoor dat jouw token privé blijft! Deel het met niemand. Hartelijk dank voor de medewerking en hopelijk tot in de server!!\nGroetjes, TI Bot :)"""

  return body


async def buildBody(user):
##build the main body
  Token = await createToken(user)

  body = """Hallo daar! \n\nWe zijn zeer blij om te horen dat je aan het proberen bent om te verifiëren dat je een student aan HOGENT bent. Om de verificatie te volbrengen, moet je het token kopieren en terugsturen naar de bot in het juiste kanaal.\n\n\tToken: """ + Token.__str__(
  ) + """\n\nStuur nu een bericht op de volgende manier in het juist kanaal in de TI server (niet in de privé chat);\n\n\t$verify [TOKEN] \n\nZorg ervoor dat jouw token privé blijft! Deel het met niemand. Hartelijk dank voor de medewerking en hopelijk tot in de server!!\nGroetjes, TI Bot :)"""

  return body

async def help(ctx):
  await ctx.channel.send(f'Hallo! Ik ben de IT Bot van de TI server. Ik kan verifieren of je student of medewerker bent bij HOGENT. Mijn commandos:\n$hey (Start het verificatieproces)\n$student [EMAIL] (dit commando werkt enkel in privéchat)\n$verify [TOKEN] (verifieert jouw emailadres via de token)\n$bugs (Geeft meer uitleg over hoe je bugs kan aangeven)')