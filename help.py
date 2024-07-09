# help.py
import discord # 기본 1
from discord.ext import commands # 기본 2
import asyncio # 기본 3

import time

async def guide(ctx):
    embed = discord.Embed(title="데마시아 가이드", description="데마시아 가이드에요!\n잘 읽고 준수해주길 바라요!", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
    embed.add_field(name="기본", value="`가이드`, `시간`", inline=False)
    embed.add_field(name="음악", value="`재생`, `일시정지`, `반복`, `플레이리스트`, `삭제`, `넘기기`, `종료`", inline=False)
    embed.add_field(name="게임", value="`주사위`, `로또`, `마피아`", inline=False)
    embed.add_field(name="시스템", value="`리그오브레전드`, `개발자정보`", inline=False)
    embed.set_footer(text="데마시아의 외교관", icon_url="https://media.discordapp.net/attachments/898797966666637354/964197572585590804/profile.jpg")
    await ctx.send(embed=embed) #embed를 포함 한 채로 메시지를 전송합니다.

async def nowtime(ctx):
    now = time.strftime('%Y-%m-%d-%p-%I-%M-%S', time.localtime(time.time()))
    await ctx.send(f"[{now[:4]}-{now[5:7]}-{now[8:10]}] {now[11:13]} {now[14:16]}시 {now[17:19]}분 {now[20:22]}초 에요!")