# The handler for mod mail
import discord
from hash_maps import HashTable

class ModMail:
  hash_tables = HashTable(2000)  # Hash table for mod-mail
  client = None
  color = None
  debug = False # Debug mode
  modmail_log_channel = None

  def __init__(self, color, client, modmail_log_channel):
    self.color = color
    self.client = client
    self.modmail_log_channel = modmail_log_channel
    
  # Handle a private msg
  async def handle_private_msg(self, message):
    if self.hash_tables.get_val(message.author.name) != 'No record found':
      staffChannel = self.hash_tables.get_val(message.author.name)
      embed=discord.Embed(title='Message from ' + message.author.name + ':', description=message.content, color=self.color)
      embed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
      DMChannel = message.channel
      userEmbed=discord.Embed(title='Your Message:', description=message.content, color=self.color)
      userEmbed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
      await staffChannel.send(embed=embed)
      await DMChannel.send(embed=userEmbed)
      return
    
    if self.debug:
      channel=self.client.get_channel(modmail_log_channel)
      await channel.send('A new message was received from **' + message.author.name + '**.')
      
    modMailChannel = await channel.guild.create_text_channel(name=message.author.name +'-mod-mail', category=channel.category)
    
    self.hash_tables.set_val(message.author.name, modMailChannel)
    self.hash_tables.set_val(modMailChannel, message.author)
    
    channel = self.hash_tables.get_val(message.author.name)
    
    staffEmbed=discord.Embed(title='Message from ' + message.author.name + ':', description=message.content, color=self.color)
    staffEmbed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
    
    userEmbed=discord.Embed(title='Your Message:', description=message.content, color=self.color)
    userEmbed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
    
    await channel.send(embed=staffEmbed)
    await message.author.send(embed=userEmbed)
    await message.channel.send('**Your message has been sent to mod-mail!**')
    
    
  # Handle a staff mod mail message
  async def handle_mod_mail_channel_msg(self, message):
    userEmbed=discord.Embed(title='Message from ' + message.author.name, description=message.content, color=self.color)
    member = self.hash_tables.get_val(message.channel)
    userEmbed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)

    staffEmbed=discord.Embed(title='Message sent by ' + message.author.name, description=message.content, color=self.color)
    staffEmbed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
    await member.send(embed=userEmbed)
    await message.delete()
    await message.channel.send(embed=staffEmbed)
    

  # Handle a mod mail channel close
  async def handle_close_mod_mail(self, message):
    if message.channel.name.endswith('-mod-mail'):
      self.hash_tables.delete_val(self.hash_tables.get_val(message.channel.name))
      self.hash_tables.delete_val(message.channel)

      if debug:
        print('[LOGS] A mod mail channel was deleted')
        
      await message.channel.delete()
    
