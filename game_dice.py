# game_dice.py
import discord # 기본 1
from discord.ext import commands # 기본 2
import asyncio # 기본 3

import random

Diceimage = ["0",
"https://media.discordapp.net/attachments/898797966666637354/998218730452549692/Dice_1.jpg",
"https://media.discordapp.net/attachments/898797966666637354/998218744054697994/Dice_2.jpg",
"https://media.discordapp.net/attachments/898797966666637354/998218749108830298/Dice_3.jpg",
"https://media.discordapp.net/attachments/898797966666637354/998218945196728360/Dice_4.jpg",
"https://media.discordapp.net/attachments/898797966666637354/998218950364111010/Dice_5.jpg",
"https://media.discordapp.net/attachments/898797966666637354/998218963538419752/Dice_6.jpg"]


# 주사위 게임
async def dice_game(ctx):
    await ctx.send("주사위를 굴리는중...")
    await asyncio.sleep(2)
    Dice = random.randint(1,6)
    embed = discord.Embed(title=f"주사위 결과는 {Dice}입니다!")
    embed.set_image(url=Diceimage[Dice])
    embed.set_footer(text="데마시아의 외교관", icon_url="https://media.discordapp.net/attachments/898797966666637354/964197572585590804/profile.jpg")
    await ctx.send(embed=embed)