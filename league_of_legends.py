# league_of_legends.py
import discord # 기본 1
from discord.ext import commands # 기본 2
import asyncio # 기본 3

import json
import requests

from system import api_key

async def league_of_legends_api(ctx, message):
    if(message == None): 
        embed = discord.Embed(title="리그오브레전드 전적 검색 명령어", description="명령어로 =롤 =전적 =lol =LOL 사용 가능\n솔로랭크, 자유랭크, TFT더블업 정보 제공 (한 판도 플레이 하지 않을시 제공 X)", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
        embed.add_field(name="전적 검색", value="`=리그오브레전드 <닉네임>`", inline=False)
        embed.add_field(name="챔피언 검색", value="`=챔피언 <챔피언 명>`", inline=False)
        embed.set_footer(text="데마시아의 외교관", icon_url="https://media.discordapp.net/attachments/898797966666637354/964197572585590804/profile.jpg")
        await ctx.send(embed=embed)
    else:
        nickname = message
        URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+nickname
        res = requests.get(URL, headers={"X-Riot-Token": api_key})
        if res.status_code == 200:
            #코드가 200일때
            resobj = json.loads(res.text)
            URL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+resobj["id"]
            res = requests.get(URL, headers={"X-Riot-Token": api_key})
            rankinfo = json.loads(res.text)
            if len(rankinfo) == 0:
                await ctx.send("솔로랭크/자유랭크 전적 기록이 없는 소환사 입니다.")
            else:
                #rankdict = {"RANKED_SOLO_5x5":0,"RANKED_FLEX_SR":1,"RANKED_TFT_DOUBLE_UP":2}
                #rankinfo.sort(key=lambda x: rankdict[x]) # 솔랭 - 자랭 - TFT 순으로 정렬
                SOLOtoken = False
                FLEXtoken = False
                TFTDBtoken = False
                for i in rankinfo:
                    if i["queueType"] == "RANKED_SOLO_5x5":
                        embed1 = discord.Embed(title="⭐ 솔로랭크", color=0x62c1cc)
                        embed1.add_field(name="소환사 이름", value=(f"`{nickname}`"), inline=False)
                        embed1.add_field(name="티어", value=(f'{i["tier"]} {i["rank"]}'), inline=True)
                        embed1.add_field(name="승률", value=(f'승: {i["wins"]}판, 패: {i["losses"]}판【`{i["wins"]/(i["wins"]+i["losses"])*100:.1f}%`】'), inline=True)
                        embed1.set_footer(text="데마시아의 외교관", icon_url="https://media.discordapp.net/attachments/898797966666637354/964197572585590804/profile.jpg")
                        SOLOtoken=True
                    elif i["queueType"] == "RANKED_FLEX_SR":
                        embed2 = discord.Embed(title="🌙 자유랭크", color=0x62c1cc)
                        embed2.add_field(name="소환사 이름", value=(f"`{nickname}`"), inline=False)
                        embed2.add_field(name="티어", value=(f'{i["tier"]} {i["rank"]}'), inline=True)
                        embed2.add_field(name="승률", value=(f'승: {i["wins"]}판, 패: {i["losses"]}판【`{i["wins"]/(i["wins"]+i["losses"])*100:.1f}%`】'), inline=True)
                        embed2.set_footer(text="데마시아의 외교관", icon_url="https://media.discordapp.net/attachments/898797966666637354/964197572585590804/profile.jpg")
                        FLEXtoken=True
                    else:
                        embed3 = discord.Embed(title="🌠 TFT 더블업", color=0x62c1cc)
                        embed3.add_field(name="소환사 이름", value=(f"`{nickname}`"), inline=False)
                        embed3.add_field(name="티어", value=(f'{i["tier"]} {i["rank"]}'), inline=True)
                        embed3.add_field(name="승률", value=(f'승: {i["wins"]}판, 패: {i["losses"]}판【`{i["wins"]/(i["wins"]+i["losses"])*100:.1f}%`】'), inline=True)
                        embed3.set_footer(text="데마시아의 외교관", icon_url="https://media.discordapp.net/attachments/898797966666637354/964197572585590804/profile.jpg")
                        TFTDBtoken=True
                if SOLOtoken == True:
                    await ctx.send(embed=embed1)
                if FLEXtoken == True:
                    await ctx.send(embed=embed2)
                if TFTDBtoken == True:
                    await ctx.send(embed=embed3)
        else:
            await ctx.send("소환사가 존재하지 않습니다")