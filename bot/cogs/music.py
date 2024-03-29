import re
import discord
import typing as t
import wavelink
import asyncio
from discord.ext import commands
import constants
from discord import app_commands
import datetime

TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"

class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.queue = []
		self.position = 0
		self.playingTextChannel = 0
	
	async def setup(self):
		await wavelink.NodePool.create_node(bot=self.bot,
                                            host='127.0.0.1',
                                            port=2333,
                                            password='youshallnotpass',
                                            region="europe")
	
	@commands.Cog.listener()
	async def on_wavelink_node_ready(self, node: wavelink.Node):
		print(f"Node <{node.identifier}> is now Ready!")

	async def cog_check(self, ctx):
		song_channel = f"{constants.SONG_CHANNEL}"
		test_channel = f"{constants.TEST_CHANNEL}"
		if str(ctx.channel.id) == (test_channel):
			return True
		if str(ctx.channel.id) != (song_channel):
			await ctx.send(f"Please go to song channel :arrow_right: <#{constants.SONG_CHANNEL}>")
			return False
		return True
	
	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		voice_state = member.guild.voice_client
		if voice_state is None:
			return
		if len(voice_state.channel.members) == 1:
			await voice_state.disconnect()
			self.queue.clear()
		if before.channel and not after.channel and member.id == constants.BOT_ID:
			song_channel = self.bot.get_channel(constants.SONG_CHANNEL)
			await song_channel.send("Disconnected :wave:")
			await voice_state.disconnect()
			self.queue.clear()

	@commands.Cog.listener()
	async def on_wavelink_track_start(self, player: wavelink.Player, track: wavelink.Track):
		try:
					
			channel = self.bot.get_channel(constants.SONG_CHANNEL)
			embed=discord.Embed(
					title=f"Playing now",
					description=f"[{track.title}]({player.track.info['uri']})",
					timestamp=datetime.datetime.now(),
					color=discord.Color.from_rgb(0,255,0))
			if (len(self.queue)-1) < 0:
				pass
			else:
				embed.add_field(name="Queue", value=f"`{len(self.queue)-1} songs`")
			await channel.send(embed=embed)
			self.queue.pop(0)
		except:
			pass
	
	@commands.Cog.listener()
	async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
		if str(reason) == "FINISHED":
			if not len(self.queue) == 0:
				next_track: track = self.queue[0]
				channel = self.bot.get_channel(constants.SONG_CHANNEL)

				try:
					await player.play(next_track)
				except:
					return await channel.send(
						embed=discord.Embed(title=f"Something went wrong while playing **{next_track.title}**",
						color=discord.Color.from_rgb(255,0,0)))
			else:
				pass
		else:
			print(reason)

	@commands.hybrid_command(name="join", with_app_command=True ,description="Add bot to your voice channel")
	@app_commands.guilds(constants.SERVER_ID)
	@app_commands.describe(channel="Voice channel name not needed")
	async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
		voice_state = ctx.author.voice

		if voice_state is None:
			return await ctx.reply("You need to be in a voice channel to use this command")

		if channel is None:
			channel = ctx.author.voice.channel

		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)
		
		if player is not None:
			if player.is_connected():
				return await ctx.reply(f"BOT is already connected to a voice channel")

		await channel.connect(cls=wavelink.Player)
		await ctx.send(f"Connected to {channel.name}.")
		
	@commands.hybrid_command(name="leave", with_app_command=True ,description="Bot leave your voice channel")
	@app_commands.guilds(constants.SERVER_ID)
	async def leave_command(self, ctx):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)

		if player is None:
			return await ctx.reply(f"BOT is not connected to any channel")

		await player.disconnect()
		self.queue.clear()
		await ctx.send(f"Disconnected :wave:")

	@commands.hybrid_command(name="play", with_app_command=True ,description="Play your desired song")
	@app_commands.guilds(constants.SERVER_ID)
	@app_commands.describe(search="Add your favorite song title or link")
	async def play_command(self, ctx, *, search: str):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)
		voice_state = ctx.author.voice

		if voice_state is None:
			return await ctx.reply("You need to be in a voice channel to use this command")

		elif (player is None):
			channel = ctx.author.voice.channel
			await ctx.author.voice.channel.connect(cls=wavelink.Player)
			await ctx.send(f"Connected to `{channel.name}`")
		try:
			tracks = await wavelink.YouTubeTrack.search(query=search)
		except:
			return await ctx.reply(embed=discord.Embed(title="Something went wrong while searching for this track", color=discord.Color.from_rgb(255,0,0)))

		if tracks is None:
			return await ctx.reply("No tracks found")

		mbed = discord.Embed(
			title="Select the track: ",
			description=("\n".join(f"**{i+1}.** {t.title}" for i, t in enumerate(tracks[:5]))),
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
		
		if not len(self.queue) == 0:
			mbed = discord.Embed(
				title=f"**`{choosed_track}`** Added To the queue",
				color=discord.Color.from_rgb(255, 255, 255)
			)
			await ctx.send(embed=mbed)
	
	
	@play_command.error
	async def play_command_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			embed=discord.Embed(title="ERROR", description=f"Please provide a song", color=0xff0000)
			await ctx.reply(embed=embed)

	@commands.hybrid_command(name="playlist", with_app_command=True ,description="Play your favorite playlist")
	@app_commands.guilds(constants.SERVER_ID)
	@app_commands.describe(search="Add your favorite playlist link")
	async def playlist_command(self, ctx, *, search: wavelink.YouTubePlaylist):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)
		voice_state = ctx.author.voice

		if voice_state is None:
			return await ctx.reply("You need to be in a voice channel to use this command")

		if player is None:
			channel = ctx.author.voice.channel
			await ctx.author.voice.channel.connect(cls=wavelink.Player)
			await ctx.send(f"Connected to `{channel.name}`")

		if search is None:
			return await ctx.reply("Please provide a playlist link")
		else:
			if not ctx.voice_client:
				vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
			else:
				vc: wavelink.Player = ctx.voice_client

			self.queue.clear()
			if vc.is_playing():
				await vc.stop();
			for songs in search.tracks:
				self.queue.append(songs)
			
			if not vc.is_playing():
				next_track: wavelink.Track = self.queue[0]
				try:
					await vc.play(next_track)
				except:
					return await ctx.reply(embed=discord.Embed(title="Something went wrong while playing this track", color=discord.Color.from_rgb(255,0,0)))
			mbed = discord.Embed(
					title=f"Now playing : `{search}`",
					description = f"Playlist with `{len(self.queue)} songs` added",
					color=discord.Color.from_rgb(255, 255, 255)
				)
			await ctx.send(embed=mbed)

	@playlist_command.error
	async def playlist_command_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			embed=discord.Embed(title="ERROR", description=f"Please provide a playlist link", color=0xff0000)
			await ctx.reply(embed=embed)
		elif isinstance(error, commands.BadArgument):
			embed=discord.Embed(title="ERROR", description=f"Please provide a playlist link", color=0xff0000)
			await ctx.reply(embed=embed)

	@commands.hybrid_command(name="stop", with_app_command=True ,description="Stop the music")
	@app_commands.guilds(constants.SERVER_ID)
	async def stop_command(self, ctx):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)

		if player is None:
			return await ctx.send("BOT is not connected to any voice channel")
		
		self.queue.clear()

		if player.is_playing:
			await player.stop()
			mbed = discord.Embed(title="Playback Stopped :stop_button:", color=discord.Color.from_rgb(255,0,0))
			return await ctx.send(embed=mbed)
		else:
			return await ctx.send("Nothing Is playing right now")

	@commands.hybrid_command(name="pause", with_app_command=True ,description="Pause the music")
	@app_commands.guilds(constants.SERVER_ID)
	async def pause_command(self, ctx):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild) 

		if player is None:
			return await ctx.send("BOT is not connected to any voice channel")

		if not player.is_paused():
			if player.is_playing():
				await player.pause()
				mbed = discord.Embed(title="Playback paused :pause_button:", color=discord.Color.from_rgb(255,165,0))
				await ctx.send(embed=mbed)
			else:
				await ctx.send("Nothing is playing right now")
		else:
			return await ctx.send("Playback is Already paused")
	
	@commands.hybrid_command(name="resume", with_app_command=True ,description="Resume paused music")
	@app_commands.guilds(constants.SERVER_ID)
	async def resume_command(self, ctx):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)

		if player is None:
			return await ctx.send("BOT is not connected to any voice channel")
		
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
	
	@commands.hybrid_command(name="playing", with_app_command=True ,description="Printing info about current song")
	@app_commands.guilds(constants.SERVER_ID)
	async def now_playing_command(self, ctx):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)
		
		if player is None:
			return await ctx.reply("BOT is not connected to any voice channel")

		if player.is_playing():
			mbed = discord.Embed(
				title=f"Playing Now",
				description=f"[{player.track}]({player.track.info['uri']})",
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

			mbed.add_field(name="Artist", value=player.track.info['author'], inline=True)
			mbed.add_field(name="Length", value=f"{length}", inline=True)
			mbed.add_field(name="Position", value=f"{position}/{length}", inline=True)
			mbed.add_field(name="Queue", value=f"`{len(self.queue)} songs`", inline=True)
			return await ctx.reply(embed=mbed)
		else:
			await ctx.reply("Nothing is playing right now")
	
	@commands.hybrid_command(name="skip", with_app_command=True ,description="Skip current song")
	@app_commands.guilds(constants.SERVER_ID)
	async def skip_command(self, ctx):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)

		if not len(self.queue) == 0:
			next_track: wavelink.Track = self.queue[0]
			try:
				await player.play(next_track)
				await ctx.reply(embed=discord.Embed(
					title="Song skipped :track_next:",
					color=discord.Color.from_rgb(0,255,0)
				))
			except:
				return await ctx.reply(embed=discord.Embed(
					title="Something went wrong while playing this track",
					color=discord.Color.from_rgb(255,0,0)
				))
		else:
			await ctx.reply("The queue is empty")
			
	@commands.hybrid_command(name="queue", with_app_command=True ,description="Print queued songs", aliases=["q"] )
	@app_commands.guilds(constants.SERVER_ID)
	@app_commands.describe(clear="Type clear if you want to clear the queue")
	async def queue_command(self, ctx: commands.Context, *, clear=None):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)
		if clear == "clear":
			if len(self.queue)==0:
				return await ctx.reply(embed=discord.Embed(title="The queue is empty", color=discord.Color.from_rgb(255, 255, 255)))
			else:
				self.queue.clear()
				return await ctx.reply(embed=discord.Embed(title="Queue cleared successfully", color=discord.Color.from_rgb(0, 255, 0)))

		if not len(self.queue) == 0:
			mbed = discord.Embed(
			title=f"Now playing: {player.track}" if player.is_playing else f"Queue: ",
			url=f"{player.track.info['uri']}",
			description = "\n".join(f"**{i+1}. {track}**" for i, track in enumerate(self.queue[:10])) 
				if not player.is_playing else f"**Queue: `{len(self.queue)} total songs`**\n"+"\n".join(f"**{i+1}.** {track}" for i, track in enumerate(self.queue[:10])),
			color=discord.Color.from_rgb(0,255,0)
			)
			return await ctx.reply(embed=mbed)
		else:
			return await ctx.reply(embed=discord.Embed(title="The queue is empty", color=discord.Color.from_rgb(255, 255, 255)))
	

	@commands.hybrid_command(name="seek", with_app_command=True ,description="Seek the music track by second or minutes")
	@app_commands.guilds(constants.SERVER_ID)
	@app_commands.describe(position="Position ex. 20s or 1m2s, seconds or minutes")
	async def seek(self, ctx: commands.Context, position: str):
		node = wavelink.NodePool.get_node()
		player = node.get_player(ctx.guild)

		if player is None:
			return await ctx.reply(embed=discord.Embed(title="BOT not connected to channel.", color=discord.Color.from_rgb(255, 0, 0)))
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
	music_bot = Music(bot)
	await bot.add_cog(music_bot)
	await music_bot.setup() 