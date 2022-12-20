import re
import discord
import typing as t
import wavelink
import asyncio
from discord.ext import commands

TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"

class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.queue = []
		self.position = 0
		self.playingTextChannel = 0
		bot.loop.create_task(self.create_nodes())
	
	async def create_nodes(self):
		await self.bot.wait_until_ready()
		await wavelink.NodePool.create_node(bot=self.bot,
                                            host='127.0.0.1',
                                            port=2333,
                                            password='youshallnotpass',
                                            region="europe")
	
	@commands.Cog.listener()
	async def on_wavelink_node_ready(self, node: wavelink.Node):
		print(f"Node <{node.identifier}> is now Ready!")

	async def cog_check(self, ctx):
		song_channel = "692020480353501247"
		test_channel = "778555669590048798"
		if str(ctx.channel.id) == (test_channel):
			return True
		if str(ctx.channel.id) != (song_channel):
			await ctx.send("Please go to song channel :arrow_right: <#692020480353501247>")
			return False
		return True
	
	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		node = wavelink.NodePool.get_node()
		if not member.bot and after.channel is None:
			if not [m for m in before.channel.members if not m.bot]:
				await node.get_player(member.guild).disconnect()

	@commands.Cog.listener()
	async def on_wavelink_track_start(self, player: wavelink.Player, track: wavelink.Track):
		try:
			self.queue.pop(0)
		except:
			pass
	
	@commands.Cog.listener()
	async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
		if str(reason) == "FINISHED":
			if not len(self.queue) == 0:
				next_track: wavelink.Track = self.queue[0]
				channel = self.bot.get_channel(692020480353501247)

				try:
					await player.play(next_track)
				except:
					return await channel.send(
						embed=discord.Embed(title=f"Something went wrong while playing **{next_track.title}**",
						color=discord.Color.from_rgb(255,0,0)))
				await channel.send(embed=discord.Embed(
					title=f"Now Playing: {next_track.title}",
					url=f"{player.track.info['uri']}",
					color=discord.Color.from_rgb(0,255,0)))
			else:
				pass
		else:
			print(reason)

	@commands.command(name="connect", aliases=["join"])
	async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
		if channel is None:
			channel = ctx.author.voice.channel

		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)
		
		if player is not None:
			if player.is_connected():
				return await ctx.send(f"{ctx.author.mention} BOT is already connected to a voice channel")

		await channel.connect(cls=wavelink.Player)
		await ctx.send(f"Connected to {channel.name}.")
		
	@commands.command(name="leave", aliases=["disconnect"])
	async def leave_command(self, ctx):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)

		if player is None:
			return await ctx.send(f"{ctx.author.mention}, Bot is not connected to any channel")

		await player.disconnect()
		await ctx.send(f"Disconnected :wave:")

	@commands.command(name="play", aliases=['p'])
	async def play_command(self, ctx, *, search: t.Optional[str]):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)
		
		if player is None:
			channel = ctx.author.voice.channel
			await ctx.author.voice.channel.connect(cls=wavelink.Player)
			await ctx.send(f"Connected to `{channel.name}`")

		if search is None:
			if player.is_paused():
				await player.resume()
				mbed = discord.Embed(title="Playback resumed :arrow_forward:", color=discord.Color.from_rgb(0,255,0))
				return await ctx.send(embed=mbed)
			else:
				return await ctx.reply("Please provide a song to search")	
		
		try:
			tracks = await wavelink.YouTubeTrack.search(query=search)
		except:
			return await ctx.reply(embed=discord.Embed(title="Something went wrong while searching for this track", color=discord.Color.from_rgb(255,0,0)))

		if tracks is None:
			return await ctx.reply("No tracks found")

		mbed = discord.Embed(
			title="Select the track: ",
			description=("\n".join(f"**{i+1}. {t.title}**" for i, t in enumerate(tracks[:5]))),
			color = discord.Color.from_rgb(255, 255, 255)
		)
		msg = await ctx.reply(embed=mbed)

		emojis_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '❌']
		emojis_dict = {
			'1️⃣': 0,
			"2️⃣": 1,
			"3️⃣": 2,
			"4️⃣": 3,
			"5️⃣": 4,
			"❌": -1
		}

		for emoji in list(emojis_list[:min(len(tracks), len(emojis_list))]):
			await msg.add_reaction(emoji)

		def check(res, user):
			return(res.emoji in emojis_list and user == ctx.author and res.message.id == msg.id)

		try:
			reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
		except asyncio.TimeoutError:
			await msg.delete()
			return
		else:
			await msg.delete()

		try:
			if emojis_dict[reaction.emoji] == -1: return
			choosed_track = tracks[emojis_dict[reaction.emoji]]
		except:
			return
	
		if not ctx.voice_client:
			vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
		else:
			vc: wavelink.Player = ctx.voice_client

		if not vc.is_playing():
			try:
				await vc.play(choosed_track)
			except:
				return await ctx.reply(embed=discord.Embed(title="Something went wrong while playing this track", color=discord.Color.from_rgb(255,0,0)))
		else:
			self.queue.append(choosed_track)
		mbed = discord.Embed(
				title=f"Added {choosed_track} To the queue",
				color=discord.Color.from_rgb(255, 255, 255)
			)
		await ctx.send(embed=mbed)

	@commands.command(name="stop")
	async def stop_command(self, ctx):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)

		if player is None:
			return await ctx.send("Bot is not connected to any voice channel")
		
		self.queue.clear()

		if player.is_playing:
			await player.stop()
			mbed = discord.Embed(title="Playback Stopped :stop_button:", color=discord.Color.from_rgb(255,0,0))
			return await ctx.send(embed=mbed)
		else:
			return await ctx.send("Nothing Is playing right now")

	@commands.command(name="pause")
	async def pause_command(self, ctx):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild) 

		if player is None:
			return await ctx.send("Bot is not connected to any voice channel")

		if not player.is_paused():
			if player.is_playing():
				await player.pause()
				mbed = discord.Embed(title="Playback paused :pause_button:", color=discord.Color.from_rgb(255,165,0))
				await ctx.send(embed=mbed)
			else:
				await ctx.send("Nothing is playing right now")
		else:
			return await ctx.send("Playback is Already paused")

	@commands.command(name="resume")
	async def resume_command(self, ctx):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)

		if player is None:
			return await ctx.send("Bot is not connected to any voice channel")
		
		if player.is_paused():
			await player.resume()
			mbed = discord.Embed(title="Playback resumed :arrow_forward:", color=discord.Color.from_rgb(0,255,0))
			return await ctx.send(embed=mbed)
		else:
			if not len(self.queue) == 0:
				track: wavelink.Track = self.queue[0]
				await player.play(track)
				return await ctx.reply(embed=discord.Embed(
					title=f"Now Playing: {track.title}"))
			else:
				return await ctx.send("Playback is not paused")
	
	@commands.command(name="playing")
	async def now_playing_command(self, ctx):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)
		
		if player is None:
			return await ctx.reply("Bot is not connected to any voice channel")

		if player.is_playing():
			mbed = discord.Embed(
				title=f"Now Playing: {player.track}",
				url=f"{player.track.info['uri']}",
				color=discord.Color.from_rgb(0,255,0)
			)

			t_sec = int(player.track.length)
			hour = int(t_sec/3600)
			min = int((t_sec%3600)/60)
			sec = int((t_sec%3600)%60)
			length = f"{hour}hr {min}min {sec}sec" if not hour == 0 else f"{min}min {sec}sec"
			
			pos_sec= int(player.position)
			pos_hour = int(pos_sec/3600)
			pos_min = int((pos_sec%3600)/60)
			pos_sec = int((pos_sec%3600)%60)
			position = f"{pos_hour}hr {pos_min}min {pos_sec}sec" if not hour == 0 else f"{pos_min}min {pos_sec}sec"

			mbed.add_field(name="Artist", value=player.track.info['author'], inline=False)
			mbed.add_field(name="Length", value=f"{length}", inline=False)
			mbed.add_field(
				name="Position",
				value=f"{position}/{length}",
				inline=False
			)
			return await ctx.reply(embed=mbed)
		else:
			await ctx.reply("Nothing is playing right now")
	
	@commands.command(name="skip", aliases=['next'])
	async def skip_command(self, ctx):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)

		if not len(self.queue) == 0:
			next_track: wavelink.Track = self.queue[0]
			try:
				await player.play(next_track)
			except:
				return await ctx.reply(embed=discord.Embed(
					title="Something went wrong while playing this track",
					color=discord.Color.from_rgb(255,0,0)
				))
			await ctx.reply(embed=discord.Embed(
				title=f"Now Playing {next_track.title}",
				url=f"{player.track.info['uri']}",
				color=discord.Color.from_rgb(0,255,0)
			))
		else:
			await ctx.reply("The queue is empty")
			
	@commands.command(name="queue", aliases=["q"])
	async def queue_command(self, ctx: commands.Context, *, search=None):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)
		
		if search is None:
			if not len(self.queue) == 0:
				mbed = discord.Embed(
				title=f"Now playing: {player.track}" if player.is_playing else "Queue: ",
				url=f"{player.track.info['uri']}",
				description = "\n".join(f"**{i+1}. {track}**" for i, track in enumerate(self.queue[:10])) 
					if not player.is_playing else "**Queue: **\n"+"\n".join(f"**{i+1}. {track}**" for i, track in enumerate(self.queue[:10])),
				color=discord.Color.from_rgb(0,255,0)
				)

				return await ctx.reply(embed=mbed)
			else:
				return await ctx.reply(embed=discord.Embed(title="The queue is empty", color=discord.Color.from_rgb(255, 255, 255)))
		else:
			try:
				track = await wavelink.YoutubeTrack.search(query=search, return_first=True)
			except:
				return await ctx.reply(embed=discord.Embed(title="Something went wrong while searching for this track", color=discord.Color.from_rgb(255,0,0)))
		
		if not ctx.voice_client:
			vc: wavelink.Player = await ctx.author.voice.channel(cls=wavelink.Player)
			await player.connect(ctx.author.voice.channel)
		else:
			vc: wavelink.Player = ctx.voice_client
		
		if not vc.is_playing():
			try:
				await vc.play(track)
			except:
				return await ctx.reply(embed=discord.Embed(title="Something went wrong while playing this track", color=discord.Color.from_rgb(255,0,0)))
		else:
			self.queue.append(track)
		
		await ctx.reply(embed=discord.Embed(title=f"Added {track.title} to the queue", color=discord.Color.from_rgb(255, 255, 255)))

	@commands.command(name="seek")
	async def seek(self, ctx: commands.Context, position: str):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)

		if player is None:
			return await ctx.reply(embed=discord.Embed(title="Bot not connected to channel.", color=discord.Color.from_rgb(255, 0, 0)))
		else:	
			if player.is_playing():
				if not(match := re.match(TIME_REGEX, position)):
					return await ctx.reply("Invalid time entry")
				if match.group(3):
					secs = (int(match.group(1)) * 60) + (int(match.group(3)))
				else:
					secs = int(match.group(1))
				await player.seek(secs * 1000)

				mbed = discord.Embed(
					title=f"Seeked To {position}",
					color = discord.Color.from_rgb(0, 255, 0)
				)
				await ctx.send(embed=mbed)
			else:
				return await ctx.reply("Nothing Is playing right now")

	@seek.error
	async def seek_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			embed=discord.Embed(title="User ERROR", description=f"Please enter time.", color=discord.Color.from_rgb(255, 0, 0))
			await ctx.repy(embed=embed)

async def setup(bot):
	await bot.add_cog(Music(bot)) 