import discord
import time
from mod_mail_handler import ModMail
from mcstatus import JavaServer
import configuration as config

server = JavaServer.lookup(config.server_ip) # The java server
client = discord.Client() # The bot client
modmail = ModMail(config.color, client, config.modmail_log_channel) # The mod mail manager

@client.event
async def on_ready():
  print('The bot has logged in as {0.user}'.format(client))
  await set_status()

# Setting the bot status
async def set_status():
  time.sleep(3)
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!help and DMs'))

# Handle the bot help msg
async def handle_help(message):
  embed=discord.Embed(title=config.bot_name + ' - Help Page', url='http://' + config.website, description='These are all the commands of the' + config.bot_name + 'bot.', color=config.color)
  embed.add_field(name='!ip', value='Displays the server ip.', inline=False)
  embed.add_field(name='!links', value='Displays various links.', inline=False)
  embed.add_field(name='!invite', value='Sends an invite link to the discord', inline=False)
  embed.add_field(name='!suggest <suggestion>', value='Sends your suggestion to the suggestions channel.', inline=False)
  embed.add_field(name='!support', value='Tells you how to get support/report a bug/report a user', inline=False)
  embed.add_field(name='!status', value='Displays the online status of the server', inline=False)
  embed.add_field(name='!players', value='Displays the player count of the server', inline=False)
  await message.channel.send(embed=embed)

# Handle suggestions
async def handle_suggestion(message):
  suggestionData = '{}'.format(message.content).replace('!suggest', ' ')
  embed=discord.Embed(title = 'New Suggestion!:')
  embed.add_field(name='Vote Below!', value=suggestionData, inline=True)
  channel=client.get_channel(config.suggestion_channel)
  embed.color=config.color
  embed.set_footer(text='Suggested by ' + message.author.name, icon_url=message.author.avatar_url)
  up_emoji = '\N{THUMBS UP SIGN}'
  down_emoji = '\N{THUMBS DOWN SIGN}'
  msg = await channel.send(embed=embed)

  await msg.add_reaction(up_emoji)
  await msg.add_reaction(down_emoji)

  await message.channel.send('Your suggestion has been submittted ' + '**' + message.author.name + '**')

# Handle links
async def handle_links(message):
  embed=discord.Embed(title = 'Links:')
  embed.add_field(name='Website/Forums:', value='http://' + config.website, inline=False)
  embed.add_field(name='Ban Appeal:', value='http://' + config.ban_appeal, inline=False)
  embed.add_field(name='Staff Application:', value='http://' + config.staff_application, inline=False)
  embed.color=config.color
  await message.channel.send(embed=embed)

# Handle IP
async def handle_ip(message):
  embed=discord.Embed(title = 'IP:', description = '**' + config.server_ip + '**', color=config.color)
  await message.channel.send(embed=embed)

# Handle server status
async def handle_server_status(message):
  try:
    server.status()
    await message.channel.send(':green_circle: Server is online')
  except Exception:
    await message.channel.send(':red_circle: Server is offline')

# Handle player list
async def handle_players(message):
  try:
    status=server.status()
    players=status.players.online
    await message.channel.send('There are ' + players + ' players online.')
  except:
    await message.channel.send('There are 0 players online.')

# Handle support info
async def handle_support(message):
  embed=discord.Embed(title = 'Support:', description = '**To get support, report a user/player, or report a bug please dm me.**', color=config.color)
  await message.channel.send(embed=embed)

# Listen to messages for mod-mail/cmds
@client.event
async def on_message(message):

  # Ignore msgs sent by the bot
  if message.author == client.user:
    return

  # Mod-mail
  if message.content.startswith('!close'):
    await modmail.handle_close_mod_mail(message)
    return

  if modmail.hash_tables.get_val(message.channel) != 'No record found':
    await modmail.handle_mod_mail_channel_msg(message)
    return

  if str(message.channel.type) == 'private':
    await modmail.handle_private_msg(message)
    return


  # Commands
  if message.content.startswith('!status'):
    await handle_server_status(message)
    return

  if message.content.startswith('!players'):
    await handle_players(message)
    return

  if message.content.startswith('!suggest'):
    await handle_suggestion(message)
    return

  if message.content.startswith('!support'):
    await handle_support(message)
    return

  if message.content.startswith('!ip'):
    await handle_ip(message)
    return

  if message.content.startswith('!invite'):
    await message.channel.send('Invite other people with the link: ' +  config.invite_link)
    return

  if message.content.startswith('!links'):
    await handle_links(message)
    return

  if message.content.startswith('!help'):
    await handle_help(message)
    return


client.run(config.bot_token)

