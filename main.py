# main.py
import discord # 기본 1
from discord.ext import commands # 기본 2
import asyncio # 기본 3

from help import guide, nowtime # help.py
from song import print_playlist, playlist_cut, skip_song, pause_song, repeat_song, quit_song, play_song # song.py
from game_dice import dice_game # game_dice.py
from game_lotto import print_lotto_rule, setting_lotto, lotto_game # game_lotto.py
from game_mafia import mafia_game # game_mafia.py
from league_of_legends import league_of_legends_api # league_of_legends.py
from system import Token, bot # system.py

@bot.event # 시작
async def on_ready():
    print("[!] 망치를 손질하고 있습니다 ...")
    await asyncio.sleep(0.5)
    print("[!] 용기나는 바지를 챙겨입는중 ...")
    await asyncio.sleep(0.5)
    print("[!] 영웅을 찾기 위해 디스코드에 입장중 ...")
    await asyncio.sleep(0.5)
    print(f"[ {bot.user.name} ] 성공적으로 연결되었습니다!")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='=가이드'))
    # 상태 (온라인) / 활동 / 대소문자 자동 구분 case_insensitive=True (X)

# @bot.event # 잘못된 명령어 사용
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#     	await ctx.send("크흠! 말씀중에 죄송하지만 이해하지 못했어요.\n다시... 설명해주실 수 있나요?")

############################################## 【 기본 】 ##############################################

# 가이드
@bot.command(aliases = ['도움말','?','help']) #name='가이드' / #help='데마시아 가이드를 제공합니다!' / #usage='=가이드 [항목] (태그/종류)'
async def 가이드(ctx):
    await guide(ctx)

# 시간
@bot.command(aliases=['time']) 
async def 시간(ctx): 
    await nowtime(ctx)

############################################## 【 음악 】 ##############################################

# 플레이리스트
@bot.command(aliases = ['playlist','플리'])
async def 플레이리스트(ctx):
    await print_playlist(ctx)
    
# 일시정지
@bot.command(aliases = ['pause','resume'])
async def 일시정지(ctx):
    await pause_song(ctx)

# 반복
@bot.command(aliases = ['repeat','r'])
async def 반복(ctx):
    await repeat_song(ctx)

# 삭제
@bot.command(aliases = ['remove','rm'])
async def 삭제(ctx,*,number=None):
    await playlist_cut(ctx,number)

# 넘기기
@bot.command(aliases = ['skip','s','스킵'])
async def 넘기기(ctx):
    await skip_song(ctx)

# 종료
@bot.command()
async def 종료(ctx):
    await quit_song(ctx)

# 노래 재생
@bot.command(aliases = ['play','p','ㅔ','wotod'])
async def 재생(ctx,*,keyword):
    await play_song(ctx, keyword)

############################################## 【 게임 】 ##############################################

# 주사위 게임
@bot.command()
async def 주사위(ctx):
    await dice_game(ctx)

# 로또 게임
@bot.command()
async def 로또(ctx,*,message=None):
    if(message == None):
        await print_lotto_rule(ctx)
    else:
        try:
            select_number = message.split()
            select_number = list(set(map(int,select_number)))
            if len(select_number) == 6 and max(select_number) <= 45 and min(select_number) >= 1:
                await lotto_game(ctx, select_number, message)
            else:
                await ctx.send("번호를 다시 입력해주세요! 중복 없이 공백을 기준으로 1 2 3 4 5 6 처럼 입력해주세요.")
        except:
            await ctx.send("번호를 다시 입력해주세요! 중복 없이 공백을 기준으로 1 2 3 4 5 6 처럼 입력해주세요.")
        
# 로또 게임 설정
@bot.command()
async def 로또설정(ctx,*,message=None):
    await setting_lotto(ctx, message)

# 마피아 게임
@bot.command()
async def 마피아(ctx,*,message=None):
    await mafia_game(ctx, message)

############################################## 【 시스템 】 ##############################################

# 롤 전적
@bot.command(aliases=['롤','전적','lol','LOL'])
async def 리그오브레전드(ctx,*,message=None):
    await league_of_legends_api(ctx,message)

# 챔피언 정보
@bot.command()
async def 챔피언(ctx,*,message):
    await ctx.send("아직 준비중이에요!")

# 개발자 정보
@bot.command()
async def 개발자정보(ctx):
    await ctx.send("ⓒ Copyright 2022, leebarang, All right reserved")

############################################## 【 RUN 】 ##############################################

bot.run(Token)