import discord
import os
from discord.ext import commands
import smtplib
import time
from email.mime.text import MIMEText
from uuid import uuid4
from replit import db


client = discord.Client()
bot = commands.Bot(command_prefix="-")
TOKEN = os.environ['TOKEN']

StudentEmails = 'student.hogent.be'
LectorEmails = 'hogent.be'


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


##what did you message me??
@client.event
async def on_message(message):
    if message.author == client:
        return

    if message.content.startswith('-hey'):
      await sendVerifMessage(message)
        

    if message.content.startswith('-student'):
        await sendmail(message)

        ##check if the given token is the correct token
    if message.content.startswith('-verify'):
        await verify(message)

    if message.content. __eq__('-help'):
        
        await message.channel.send('Hi there! I am the verification bot. I can verify wether you are a student or a lector at HOGENT. To get more details, please send the message  -help student  or  -help lector  . If you have any problems, bugs, or tips, use the command -bugs. Hope this helps!')
        
    if message.content.startswith('-bugs'):
        myid = '<@496641850443169801>'
        await message.channel.send('If you have encountered a bug or problem with the bot, please send ' + myid +' a private message, or any other mod in the server. ')
    if message.content.startswith('-help student'):
        await sendhelp(message)

    if message.content.startswith('-help lector'):
        await sendhelplector(message)
        
async def sendVerifMessage(message):
    botmessage = await message.channel.send(
    'I have sent you a private message to verify your account')
    await message.delete()
    await message.author.send(
        "To verify that you are a student, please give us your school email. The way to do is, is to send me a message like this: -student youremail@school.be"
    )
    time.sleep(5)
    await botmessage.delete()


async def verify(message):
    possibleToken = message.content.split(' ')[1]
    student = message.author.name
    tokenName = student+'_Token'
    print(tokenName)
    Token = db[tokenName]
    if (possibleToken == Token):
        member = message.author
        role = discord.utils.get(message.guild.roles, name="Student")
        await member.add_roles(role)
        botmessage = await message.channel.send('You are verified as a student now! Check your roles!')
    else:
      botmessage = await message.channel.send('Something went wrong! Did you copy the wrong Token?')
    await message.delete()
    time.sleep(5)
    await botmessage.delete()

async def sendmail(message):
    sendmail(message)
    ##get the email school type
    schoolType = message.content.split('@')[1]
    ##If the email is any other email than the accepted school emails
    if schoolType == StudentEmails:
        ##Get email
        sender = 'tidiscordserver@gmail.com'
        Email = message.content.split(' ')[1]

        ##build email
        receiver = Email
        bodySend = await buildBody(message.author.name)
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
        await message.author.send('We have sent you an email. Please remember to check your junk folder!')
    if schoolType == LectorEmails:
        sender = 'tidiscordserver@gmail.com'
        Email = message.content.split(' ')[1]

        ##build email
        receiver = Email
        bodySend = await buildLectorBody(message.author.name)
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
        await message.author.send('We have sent you an email. Please remember to check your junk folder!')
    else:
        await message.author.send('This is not a HOGENT school email. Please check that you sent me your HOGENT email.')


async def createToken(user):
    ##create unique token to verify
    studentToken = uuid4()
    keyName = user+'_Token'
    db[keyName] = studentToken.__str__()
    return studentToken


async def createLectorToken(user):
    lectorToken = uuid4()+'l'
    keyName = user+'_Token'
    db[keyName] = lectorToken.__str__()
    return lectorToken

async def buildLectorBody(user):
    Token = await createLectorToken(user)
    body = """Hey there! \n\nWe're very pleased to hear that you are trying to verify that you are a lector or employee at HOGENT. To finish the verification, please copy the token and send it back to the bot in the TI server channel verification \n\n\tToken: """ + Token.__str__() + """\n\nPlease send the message in the following way in the channel Verification in the TI server;\n\n\t-verify [TOKEN] \n\nPlease do not share your Token with anybody! Thank you so much for your cooperation and hopefully we'll see you in the server!!\nGreetings, TI Bot :)"""

    return body
    
    
async def buildBody(user):
    ##build the main body
    Token = await createToken(user)

    body = """Hey there! \n\nWe're very pleased to hear that you are trying to verify that you are a student. To finish the verification, please copy the token and send it back to the bot in the TI server channel verification \n\n\tToken: """ + Token.__str__() + """\n\nPlease send the message in the following way in the channel Verification in the TI server;\n\n\t-verify [TOKEN] \n\nThank you so much for your cooperation and hopefully we'll see you in the server!!\nGreetings, TI Bot :)"""

    return body

async def sendhelp(message):
    await message.channel.send('Hey there! I am the verification bot. I have been built to verify if you are a student at HOGENT. To do this I follow the next steps:\n\nFirst you text me -hey . \nThen i send you a private message\nAfter that you send me your school email and after THAT i send you an email with a token. \nThis is your unique token, and when you send it back to me i know that you are the one who got the email. That way i can verify that you are a student! \n\nHope this helps!')

async def sendhelplector(message):
    await message.channel.send('Hey there! I am the verification bot. I have been built to verify if you are a lector (or employee) at HOGENT. To do this I follow the next steps:\n\nFirst you text me -hey . \nThen i send you a private message\nAfter that you send me your HOGENT email and after THAT i send you an email with a token. \nThis is your unique token, and when you send it back to me i know that you are the one who got the email. That way i can verify that you are a lector! \n\nHope this helps!')




client.run(TOKEN)
