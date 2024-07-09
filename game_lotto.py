# game.lotto.py
import discord # 기본 1
from discord.ext import commands # 기본 2
import asyncio # 기본 3

import random

chance = 1

# 로또 설명
async def print_lotto_rule(ctx):
    embed = discord.Embed(title="로또 게임", description="로또 게임에 대한 설명이에요.")
    embed.add_field(name="게임 방법", value="`=로또설정 <횟수>`, `=로또 <원하는 번호>`", inline=False)
    embed.add_field(name="주의사항", value="`원하는 번호는 1 2 3 4 5 6 이런식으로 띄워서 최대 1~45 사이 숫자로 입력해주세요.`", inline=False)
    embed.set_footer(text="데마시아의 외교관", icon_url="https://media.discordapp.net/attachments/898797966666637354/964197572585590804/profile.jpg")
    await ctx.send(embed=embed)

# 로또 설정 
async def setting_lotto(ctx, message):
    global chance
    if (message != None):
        try:
            chance = int(message)
            if chance == 1:
                await ctx.send("로또 횟수가 1로 설정되었으며, 로또 숫자가 결과와 함께 출력됩니다!")
            else:
                await ctx.send(f"로또 횟수가 {format(chance, ",")}로 설정되었습니다!\n만약 횟수가 1,000,000회 이상일 경우, 느리게 작동할 수 있습니다.")
        except:
            await ctx.send("로또 설정을 올바르게 입력해주세요, =로또 설정 <횟수>")

# 로또 게임
async def lotto_game(ctx, select_number, message):
    money = chance
    wins = [0,0,0,0,0,0] # x 1등 2등 3등 4등 5등
    for i in range(chance):
        money -= 1
        point = 0
        random_number = random.sample(range(1,46),7)
        bonus = random_number[6]
        del random_number[6]
        random_number.sort()
        for j in range(6):
            if random_number[j] in select_number:
                point += 1
            else:
                pass
        if point == 3:
            wins[5] += 1
            money += 5
        elif point == 4:
            wins[4] += 1
            money += 50
        elif point == 5:
            if bonus in select_number:
                wins[2] += 1
                money += 50000
            else:
                wins[3] += 1
                money += 1000
        elif point == 6:
            wins[1] += 1
            money += 2000000
    embed = discord.Embed(title="로또 결과")
    embed.add_field(name="총 도전 횟수", value=f"{chance}회, 현금 약 {format(chance*1000, ",")}원", inline=False)
    embed.add_field(name="시도한 번호", value=message, inline=False)
    if chance == 1:
        embed.add_field(name="당첨 번호", value=f"{random_number} (보너스번호 : {bonus})", inline=False)
        max_win_count = max(wins)
        if max_win_count == 0:
            result = '꽝입니다...'
        else:
            result = f"{wins.index(max_win_count)}등"
        embed.add_field(name="결과", value=result,inline=False)
    else:
        embed.add_field(name="결과", value=f"5등 : {wins[5]}회, 4등 : {wins[4]}회, 3등 : {wins[3]}회, 2등 : {wins[2]}회, 1등 : {wins[1]}회", inline=False)
    embed.add_field(name="수익률", value=f"당첨금 : {format(money*1000, ",")}원, 수익률 {((money-chance)/chance)*100:.1f}%", inline=False)
    embed.set_footer(text="데마시아의 외교관", icon_url="https://media.discordapp.net/attachments/898797966666637354/964197572585590804/profile.jpg")
    await ctx.send(embed=embed)