import discord, datetime, time, asyncio, random, aiohttp, async_timeout, json, re, io, urllib, sys, traceback, httplib2, \
    os, decimal
import discord
from discord.ext import commands
from discord import utils

description = '''A cute&cool bot for u all, my loved sweets <3'''
bot = commands.Bot(command_prefix='!', description=description, case_insensitive=True)
createdLimit = 10
channelJoin = {}


@bot.event
async def on_member_join(member):
    if str(member.guild.id) in channelJoin:
        embed = discord.Embed(colour=discord.Colour(
            0x00FF00) if member.created_at < datetime.datetime.now() - datetime.timedelta(days=10) else discord.Colour(
            0xFF0000))
        embed.set_author(name=str(member) + " joined", icon_url=member.avatar_url)
        embed.add_field(name='UserID', value=str(member.id), inline=True)
        embed.add_field(name='Created At', value=str(member.created_at), inline=True)
        embed.set_footer(text='New User • ' + str(member.joined_at))
        channel = bot.get_channel(channelJoin[str(member.guild.id)])
        await channel.send(embed=embed)


@bot.event
async def on_ready():
    global channelJoin
    try:
        channelJoin = json.load(open('settings.json','r'))
    except FileNotFoundError:
        print('settings.json not found')
        pass
    print('coucou')


def buildEmbed(color, author, text):
    embed = discord.Embed(colour=discord.Colour(color), title=text)
    embed.set_author(name=str(author), icon_url=author.avatar_url)
    return embed


@bot.command()
async def mvdate(ctx, limit):
    global createdLimit
    if ctx.message.author.id in [ctx.guild.owner_id, 165918545975181312]:
        if 0 <= int(limit) <= 30:
            createdLimit = int(limit)
            await ctx.send(embed=buildEmbed(0x16BFD6, ctx.message.author, 'The limit is now ' + limit + ' days'))
        else:
            await ctx.send(
                embed=buildEmbed(0x16BFD6, ctx.message.author, 'Can\'t do that sorry, that\'s beyond the limit'))


@bot.command()
async def joinmessage(ctx):
    global channelJoin
    if ctx.message.author.id in [ctx.guild.owner_id, 165918545975181312]:
        await ctx.send(embed=buildEmbed(0x16BFD6, ctx.message.author,
                                        'What channel do you want to set as channel for the join messages ?'))

        def check(m):
            return m.content in [i.mention for i in
                                 ctx.guild.channels] and m.author == ctx.author and m.channel == ctx.channel

        msg = await bot.wait_for("message", check=check, timeout=60)

        try:
            channelId = utils.get(ctx.guild.channels, mention=msg.content).id
            if str(ctx.guild.id) in channelJoin and channelJoin[str(ctx.guild.id)] == channelId:
                await ctx.send(embed=buildEmbed(0x16BFD6, ctx.message.author, 'It is already set to that channel'))
            else:
                channelJoin[str(ctx.guild.id)] = channelId
                json.dump(channelJoin, open('settings.json', 'w'))
                await ctx.send(embed=buildEmbed(0x16BFD6, ctx.message.author, 'Join message channel changed to `' + str(
                    channelJoin[str(ctx.guild.id)]) + '`'))

        except asyncio.TimeoutError:
            await ctx.send(embed=buildEmbed(0x16BFD6, ctx.message.author, 'Time is out'))


@bot.command()
async def testmemberjoin(ctx):
    await on_member_join(ctx.message.author)


@bot.command()
async def ping(ctx):
    before = time.monotonic()
    await ctx.send('Pong !')
    embed = discord.Embed(colour=discord.Colour(0x16BFD6))
    embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
    embed.add_field(name='API Latency:', value=str(
        decimal.Decimal(bot.latency).quantize(decimal.Decimal(10) ** -2)) + 'ms :signal_strength:', inline=True)
    embed.add_field(name='Bot Latency', value=str(decimal.Decimal((time.monotonic() - before) * 1000).quantize(
        decimal.Decimal(10) ** -2)) + 'ms :signal_strength:', inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def kick(ctx, member, *reason):
    if ctx.message.author.id in [ctx.guild.owner_id, 165918545975181312]:
        try:
            await utils.get(ctx.guild.members, mention=member).kick(reason=' '.join(reason))
            embed = buildEmbed(0x16BFD6, ctx.message.author, member + ' has been kicked')
            embed.description = 'for the reason : ' + ' '.join(reason)
            await ctx.send(embed=embed)
        except:
            print('I don\'t have permissions to kick')
            pass

@bot.command()
async def ban(ctx, member, *reason):
    if ctx.message.author.id in [ctx.guild.owner_id, 165918545975181312]:
        try:
            await utils.get(ctx.guild.members, mention=member).ban(reason=' '.join(reason))
            embed = buildEmbed(0x16BFD6, ctx.message.author, member + ' has been banned')
            embed.description = 'for the reason : ' + ' '.join(reason)
            await ctx.send(embed=embed)
        except:
            print('I don\'t have permissions to ban')
            pass

bot.run('NTIzMTEyOTM1NjUzMTEzODY2.DvUzNw.PW3jUUhgkHs0T4wdnJjf7FByWH0')
