import aiofiles
import discord
from discord.ext import commands

#intents = discord.Intents.default()
#intents.members = True
logChannelId = 855123222037790730

##@bot.command()
##@commands.has_permissions(administrator=True)
async def warn(ctx, bot, channel: discord.Guild=None, member: discord.Member=None, reason=None):
    if member is None:
        return await ctx.send("The provided member could not be found or you forgot to provide one.")
        
    if reason is None:
        return await ctx.send("Please provide a reason for warning this user.")

    if channel is None:
        return await ctx.send("Please provide the channel to send this warning in.")

    try:
        first_warning = False
        bot.warnings[ctx.guild.id][member.id][0] += 1
        bot.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))
        count = len(bot.warnings[ctx.guild.id][member.id][1])
        if count >= 3:
          await muteUser(ctx, bot, member, True)
        

    except KeyError:
        first_warning = True
        bot.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

    count = len(bot.warnings[ctx.guild.id][member.id][1])

    async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as file:
        await file.write(f"{member.id} {ctx.author.id} {reason}\n")

    embed = discord.Embed(title= "Warning", description=f"{member.mention} received a warning.\nReason: {reason}", colour=discord.Colour.red())
    await ctx.channel.send(f"{member.mention} has {count} {'warning' if first_warning else 'warnings'}.")
    await channel.send(embed=embed)

    ##logwarn
    logEmbed = discord.Embed(title = "Warning", description= f"{member} received a warning by {ctx.author}\n Reason: {reason}", colour = discord.Colour.red())
    await bot.get_channel(logChannelId).send(embed = logEmbed)

##@bot.command()
##@commands.has_permissions(administrator=True)
async def warnings(ctx, bot, member: discord.Member=None):
    if member is None:
        return await ctx.send("The provided member could not be found or you forgot to provide one.")
    
    

    try:
        if len(bot.warnings[ctx.guild.id][member.id][1]) > 0:
          embed = discord.Embed(title=f"Displaying Warnings for {member.name}", description="", colour=discord.Colour.red())
        else:
          raise KeyError("No warnings found")
        i = 0
        for admin_id, reason in bot.warnings[ctx.guild.id][member.id][1]:
            print(admin_id)
            admin = bot.get_user(admin_id)
            print(admin)
            embed.description += f"**Warning {i+1}** given by: <@{admin_id}> for: *'{reason}'*.\n"
            i += 1

        await ctx.send(embed=embed)

    except KeyError: # no warnings
        await ctx.send("This user has no warnings.")

async def deleteWarning(ctx, bot, reason=None, member:discord.Member=None):
    if member is None:
      return await ctx.send("The provided member could not be found or you forgot to provide one.")
    
    if reason is None:
        return await ctx.send("Please provide the reason for that warning, so i can find and delete it.")

    try:
      i=0
      for warning in bot.warnings[ctx.guild.id][member.id][1]:
        print(warning[1])
        print(reason)
        if warning[1].__eq__(reason):
          bot.warnings[ctx.guild.id][member.id][1].remove(bot.warnings[ctx.guild.id][member.id][1][i])
          

          async with aiofiles.open(f"{ctx.guild.id}.txt", mode="r") as file:
            print(file)
            lines = await file.readlines()
          async with aiofiles.open(f"{ctx.guild.id}.txt", mode="w") as f:
            for line in lines:
              print(line)
              print(f"{ctx.guild.id} {member.id} {reason}\n")
              if line.__eq__(f"{ctx.guild.id} {member.id} {reason}\n"):
                await f.write(line)
          break
        i+=1

      

      await warnings(ctx, bot, member)
      ##log
      logEmbed = discord.Embed(title = "Deleted warning", description= f"{member} had a warning removed.\n Reason of the warning was: {reason}\n Removed by: {ctx.author}", colour = discord.Colour.red())
      await bot.get_channel(logChannelId).send(embed = logEmbed)
      count = len(bot.warnings[ctx.guild.id][member.id][1])
      if count < 3:
        await muteUser(ctx,bot,member, False)
          
    except KeyError: # no warnings
        await ctx.send("This user has no warnings.")
    


async def muteUser(ctx, bot, member:discord.member, mute):
  role = discord.utils.find(lambda r: r.name == 'Muted', ctx.guild.roles)
  if role is not None:
    if(mute):
      await ctx.channel.send(f'{member.mention}, je hebt 3 of meer warnings, daardoor krijg je de mute role. Jouw situatie wordt nog nagekeken door de mods, waar zij beslissen of je een ban krijgt of niet.')
      await member.add_roles(role)
      ##log
      logEmbed = discord.Embed(title = "Member muted", description= f"{member} was given the mute role.\n Reason of being muted: >= 3 warnings\n Removed by: {ctx.author}", colour = discord.Colour.red())
      await bot.get_channel(logChannelId).send(embed = logEmbed)
    else:
      if role in member.roles:
        await ctx.channel.send(f'{member.mention}, jouw muted role is verwijdert aangezien je minder dan 3 warnings hebt.')
        await member.remove_roles(role)
        ##log
        logEmbed = discord.Embed(title = "Member unmuted", description= f"{member} was deprived of the mute role.\n Reason of being unmuted: < 3 warnings\n Removed by: {ctx.author}", colour = discord.Colour.red())
        await bot.get_channel(logChannelId).send(embed = logEmbed)


async def clearWarnings(ctx, bot, member:discord.member):
  i= len(bot.warnings[ctx.guild.id][member.id][1])
  while i > 0:
  #for warning in bot.warnings[ctx.guild.id][member.id][1]:
    print(bot.warnings[ctx.guild.id][member.id][1].pop())
    
    print(aiofiles.open(f"{ctx.guild.id}.txt", mode="a"))

    async with aiofiles.open(f"{ctx.guild.id}.txt", mode="r") as file:
      lines = await file.readlines()
    async with aiofiles.open(f"{ctx.guild.id}.txt", mode="w") as file:
      print(lines)
      for line in lines:
        words = line.split(" ")
        print(line)
        if not (words[1].__eq__(member.id)):
          print(words[1])
          print(member.id)
          await file.write(line)
    print(i)
    i-=1

  ##log
  logEmbed = discord.Embed(title = "Warnings cleared", description= f"The warnings for {member.name} were cleared", colour = discord.Colour.red())
  await bot.get_channel(logChannelId).send(embed = logEmbed)
    
  #await warnings(ctx, bot, member)

async def help(ctx):
  await ctx.channel.send(f'De commandos voor de warning bot zijn;\n $warn [CHANNEL] [MEMBER] [REASON] (Geeft een gebruiker een warning + stuurt het warningbericht in de meegegeven channel)\n $warnings [MEMBER] (Geeft alle gegeven warnings van een bepaalde user)\n $deleteWarning [MEMBER] [REASON] (Verwijdert de warning met die bepaalde reden voor de meegegeven user\n $clearWarnings [MEMBER] (Verwijdert alle warnings van de meegegeven user)')