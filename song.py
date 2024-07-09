# song.py
import discord # 기본 1
from discord.ext import commands # 기본 2
import asyncio # 기본 3
#import youtube_dl
from youtube_search import YoutubeSearch
import pytube
from pytube.innertube import _default_clients
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]
import pytube.cipher
pytube.cipher
from system import bot

playlist = []
loop = False

# 플레이리스트
async def print_playlist(ctx):
    if len(playlist) >= 1:
        embed = discord.Embed(title="💽 현재 재생중인 플레이리스트", color=0x62c1cc)
        if loop == True:
            embed.add_field(name='[현재 진행중인 곡]',value=f'🔁 【{playlist[0][0]}】', inline=False)
        elif loop == False:
            embed.add_field(name='[현재 진행중인 곡]',value=f'【{playlist[0][0]}】', inline=False)
        if len(playlist) > 1:
            for i in range(1,len(playlist)):
                embed.add_field(name=f'예약 {i}번째 곡', value=f'【{playlist[i][0]}】', inline=False)
        embed.set_thumbnail(url=playlist[0][2])
        embed.set_footer(text="데마시아의 외교관", icon_url="https://media.discordapp.net/attachments/898797966666637354/964197572585590804/profile.jpg")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="💽 현재 재생중인 플레이리스트", description='현재 재생중인 곡이 없습니다.', color=0x62c1cc)
        embed.set_footer(text="데마시아의 외교관", icon_url="https://media.discordapp.net/attachments/898797966666637354/964197572585590804/profile.jpg")
        await ctx.send(embed=embed)

# 삭제
async def playlist_cut(ctx, number):
    global playlist
    number = int(number)
    if len(playlist)-1 >= number:
        print(f"<삭제> : 【{playlist[number][0]}】")
        del playlist[number]
        await ctx.send(f"✂️{number}번째 예약곡을 삭제했어요!")
    else:
        await ctx.send(f"{number}번째 예약곡을 찾을수 없어요..")

# 넘기기
async def skip_song(ctx):
    global loop
    if len(playlist) == 0:
        await ctx.send("재생중인 곡이 없어요!")
    else:
        if loop == True:
            loop = False
            await ctx.send("넘기기를 사용하여 반복모드가 해제됩니다.")
        bot.voice_clients[0].stop()
        await ctx.send("현재 재생중인 곡을 스킵할게요!")
        if len(playlist) == 0:
            await bot.voice_clients[0].disconnect()
            await ctx.send("데마시아 노래 서비스가 끝났어요! 또 이용해주세요 헤헤.")

# 일시정지
async def pause_song(ctx):
    if len(playlist) == 0:
        await ctx.send("플레이리스트가 비어있어요.")
    else:
        if not bot.voice_clients[0].is_paused():
            bot.voice_clients[0].pause()
            await ctx.send("⏸️일시정지 되었어요! 다시 입력하면 재생됩니다 :)")
        elif bot.voice_clients[0].is_paused():
            bot.voice_clients[0].resume()
            await ctx.send("다시 재생할게요!")

# 반복
async def repeat_song(ctx):
    global loop
    if len(playlist) == 0:
        await ctx.send("플레이리스트가 비어있어요.")
    else:
        if loop == True:
            loop = False
            await ctx.send("반복모드를 해제합니다.")
        elif loop == False:
            loop = True
            await ctx.send("현재 곡을 🔁반복 설정했어요! 다시 입력하면 해제됩니다 :)")

# 종료
async def quit_song(ctx):
    global playlist
    global loop
    playlist = []
    loop = False
    if bot.voice_clients != []:
        await bot.voice_clients[0].disconnect()
    await ctx.send("데마시아 노래 서비스가 끝났어요! 또 이용해주세요 헤헤.")

# 재생
async def play_song(ctx, keyword):
    global playlist
    channel = ctx.author.voice.channel #채널 변수 생성
    if bot.voice_clients == []:
        await channel.connect()
    voice = bot.voice_clients[0]
    result = YoutubeSearch(keyword, max_results=1).to_dict() #YoutubeSearch로 키워드에 맞는 영상 캐치
    titles = result[0]['title']
    url = result[0]['url_suffix']
    songjpg = result[0]['thumbnails'][0]
    print(f'<입력> : 【{titles} 】')
    playlist.append([titles,url,songjpg]) # 플레이리스트에 수록
    await song_quest(ctx, titles, url, songjpg) # 신청-출력
    if len(playlist) == 1:
        await main_of_music(voice) #메인 보드 활성화
    else:
        pass

# 노래 사진&정보 메이킹 - quest_embed
async def song_quest(ctx, titles,url,songjpg):
    quest_embed = discord.Embed(title="𝓟𝓞𝓟𝓟𝓨'𝓼 𝓟𝓵𝓪𝔂 𝓛𝓲𝓼𝓽", description=f"⚡️데마시아에서 노래를 주문했어요!\n[클릭](https://www.youtube.com{url}) 해서 영상링크로 이동할 수 있어요!", color=0x62c1cc)
    quest_embed.add_field(name='제목',value=f'【{titles}】',inline=False)
    quest_embed.set_image(url=songjpg)
    quest_embed.set_footer(text="데마시아의 외교관", icon_url="https://media.discordapp.net/attachments/898797966666637354/964197572585590804/profile.jpg")
    await ctx.send(embed=quest_embed)

# 메인 보드 (시스템 중간처리)
async def main_of_music(voice):
    while True:
        if len(playlist) >= 1:
            await asyncio.sleep(0.1) #오류 방지 (잠시 대기)
            while voice.is_playing() or voice.is_paused():
                await asyncio.sleep(0.1)
            await song_start(voice, playlist[0][1])
        else:
            break
            #playlist = []
            #await bot.voice_clients[0].disconnect()
            #await ctx.send("데마시아 노래 서비스가 끝났어요! 또 이용해주세요 헤헤.")

# 노래 실제 재생 - 재생 시작시 플레이리스트에서 삭제
async def song_start(voice, url):
    global playlist
    stream = pytube.YouTube.streams
    itag_list = [141,140,139,251,171,250,249] # These are the lists of itags that can be played by ffmpeg.
    for itag in itag_list:
        try:
            audio = pytube.YouTube(url).streams.get_by_itag(itag).url # get stream url
            break
        except AttributeError: # cannot find stream by current itag, as itag not avaliable
            continue
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}#optimised settings for ffmpeg for streaming
    source = discord.FFmpegPCMAudio(audio, **FFMPEG_OPTIONS)  # converts the youtube audio source into a source discord can use
    voice.play(source)
    # ydl_opts = {'format': 'bestaudio'}
    # FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     info = ydl.extract_info(f'https://www.youtube.com{url}', download=False)
    #     URL = info['formats'][0]['url']
    # voice = bot.voice_clients[0]
    # voice.play(discord.FFmpegOpusAudio(URL, **FFMPEG_OPTIONS))
    while voice.is_playing() or voice.is_paused():
        await asyncio.sleep(0.1)
    if loop == True:
        pass
    elif loop == False:
        del playlist[0]