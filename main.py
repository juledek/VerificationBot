import discord
import os
from discord.ext import commands
import smtplib
from email.mime.text import MIMEText
from uuid import uuid4
from replit import db

client = discord.Client()
bot = commands.Bot(command_prefix="-")
TOKEN = os.environ['TOKEN']

listAcceptableEmails = ['student.hogent.be']


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client:
        return

    if message.content.startswith('-hey'):
        await message.channel.send(
            '-I have sent you a private message to verify your account')
        await message.author.send(
            "Give me your school email, fool! Do it this way: -verify youremail@school.be"
        )

    if message.content.startswith('-student'):
        ##get the email school type
        schoolType = message.content.split('@')[1]
        ##If the email is any other email than the accepted school emails
        if schoolType in listAcceptableEmails:
            ##Get email
            sender = 'tidiscordserver@gmail.com'
            Email = message.content.split(' ')[1]

            ##build email
            receiver = Email
            bodySend = await buildBody()
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

        ##check if the given token is the correct token
    if message.content.startswith('-verify'):
        print("trying to add role")
        possibleToken = message.content.split(' ')[1]
        studentToken = db["studentToken"]
        print("possibleToken: " + possibleToken)
        print("studentToken: " + studentToken)
        if (possibleToken == studentToken):
            print("Tokens are the same!")
            member = message.author
            role = discord.utils.get(message.guild.roles, name="Student")
            await member.add_roles(role)


async def createToken():
    ##create unique token to verify
    studentToken = uuid4()
    db["studentToken"] = studentToken.__str__()
    return studentToken


async def buildBody():
    ##build the main body
    Token = await createToken()

    body = """Hey there! \n\nWe're very pleased to hear that you are trying to verify that you are a student. To finish the verification, please copy the token and send it back to the bot in the TI server channel verification \n\n\tToken: """ + Token.__str__() + """\n\nPlease send the message in the following way in the channel Verification in the TI server;\n\n\t-verify [TOKEN] \n\nThank you so much for your cooperation and hopefully we'll see you in the server!!\nGreetings, TI Bot :)"""

    return body


client.run(TOKEN)
