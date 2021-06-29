import aiofiles
import discord
from discord.ext import commands

logChannelId = 855123222037790730
rolesChannelId = 0000000000000

async def addNewRolesMessage(ctx, bot):
  rolesChannel = bot.get_channel(logChannelId)
  rolesChannel.sendMessage()

async def getEmoji(ctx, bot, emojiId):
  try:
    emoji = ctx.guild.fetch_emoji(emoji.id)
    print(emoji)
    matching_emote = emoji
    print(bot.emojis)
  except discord.NotFound:
    return await ctx.send('couldnt find the emoji')
  return matching_emote