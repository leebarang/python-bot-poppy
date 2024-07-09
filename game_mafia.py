# game_mafia.py
import discord # 기본 1
from discord.ext import commands # 기본 2
import asyncio # 기본 3

MafiaGame = False #게임 시작 여부
Player = [] #게임 참가 인원
NumberPlayer = [] #번호가 매겨진 게임 참가 인원
GameJob = [] #게임이 진행되는 동안 가지게 될 직업
Numbertools = ['①','②','③','④','⑤','⑥','⑦','⑧','⑨']
MafiaRule = 'Classic'
MafiaRules = ['Classic','Royal','Royal_fanatic']

Mafiaimage = ["0",
"https://media.discordapp.net/attachments/898797966666637354/1001758974447714304/unknown.png",
"https://media.discordapp.net/attachments/898797966666637354/1001759450601881630/unknown.png?width=994&height=663",
"https://media.discordapp.net/attachments/898797966666637354/1001759550002704445/unknown.png?width=455&height=662",
"https://media.discordapp.net/attachments/898797966666637354/1001762405350645760/unknown.png"]

ClassicJob_4 = ['마피아','경찰','의사','시민'] # 미션 2개
ClassicJob_5 = ['마피아','경찰','의사','시민','시민'] # 미션 2개 
ClassicJob_6 = ['마피아','마피아','경찰','의사','시민','시민'] # 미션 2개
ClassicJob_7 = ['마피아','마피아','경찰','의사','시민','시민','시민'] # 미션 3개
ClassicJob_8 = ['마피아','마피아','경찰','의사','시민','시민','시민','시민'] # 미션 4개
RoyalJob_4 = ['마피아','경찰','의사','시민']
RoyalJob_5 = ['마피아','경찰','의사','시민','시민']
RoyalJob_6 = ['마피아','스파이','경찰','의사','시민','시민']
RoyalJob_7 = ['마피아','스파이','경찰','의사','시민','시민','시민']
RoyalJob_8 = ['마피아','마피아','스파이','경찰','의사','시민','시민','시민']
RoyalJob_9 = ['마피아','마피아','스파이','경찰','의사','시민','시민','시민','교주']
Citizen = ['군인','정치인','탐정','기자','성직자','연인','겜블러']

# 마피아 게임
async def mafia_game(ctx, message):
    global MafiaGame
    global Player
    global NumberPlayer
    global MafiaRule
    global MafiaDay
    global MafiaDate
    if(message == None):
        embed = discord.Embed(title="마피아 게임", description="마피아 게임에 대한 설명이에요.\n 아래 명령어들을 통해 게임에 대한 설명과, 게임 진행이 가능합니다!", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
        embed.add_field(name="게임 시작", value="`=마피아 참가`,`=마피아 시작`,`=마피아 설정`,`=마피아 초기화`", inline=False)
        embed.add_field(name="게임 설명", value="`=마피아 게임설명`,`=마피아 직업목록`", inline=False)
        embed.set_footer(text="데마시아의 외교관", icon_url="https://media.discordapp.net/attachments/898797966666637354/964197572585590804/profile.jpg")
        await ctx.send(embed=embed)
    elif(message == "참가"):
        if MafiaGame == False:
            if (ctx.author) not in Player:
                await ctx.send("{}님이 참가하셨습니다.".format(ctx.author.name))
                Player.append(ctx.author)
                NumberPlayer.append((Numbertools[len(Player)-1])+Player[len(Player)-1].name+'#'+Player[len(Player)-1].discriminator)
                await ctx.send("현재 참가 인원은 {}입니다.".format(NumberPlayer))
            else:
                await ctx.send("🚫이미 참가하셨습니다.")
        else:
            await ctx.send("🚫게임이 이미 시작되었습니다. 다음 게임이 시작될 때까지 기다려주세요.")
    elif(message == '시작'):
        if MafiaGame == False:
            await ctx.send("게임이 시작될 예정입니다 잠시만 기다려주세요. 시스템을 준비하는 동안 최대 1분이 소요됩니다.")
            if MafiaRule == 'Classic':
                if len(Player) == 1:
                    Job = ClassicJob_4.copy()
                elif len(Player) == 5:
                    Job = ClassicJob_5.copy()
                elif len(Player) == 6:
                    Job = ClassicJob_6.copy()
                elif len(Player) == 7:
                    Job = ClassicJob_7.copy()
                elif len(Player) == 8:
                    Job = ClassicJob_8.copy()
                else:
                    await ctx.send("🚫[Classic] 인원 제한이 맞지 않아 게임이 시작되지 않았습니다. (최소 4인, 최대 8인)")
                    return
                MafiaGame = True
                MafiaDay = 'Day' #Day 또는 Night으로 진행한다.
                MafiaDate = 1    #1일차
                # random.shuffle(Job)
                # 직업 분배
                for i in range(len(Player)):
                    author = Player[i]
                    if Job[i] == '마피아':
                        embed = discord.Embed(title='당신의 직업은 [마피아]입니다.', description="모두를 죽이고 승리하세요.")
                        embed.set_image(url=Mafiaimage[1])
                        embed.add_field(name="소속", value="마피아 팀", inline=False)
                    elif Job[i] == '경찰':
                        embed = discord.Embed(title='당신의 직업은 [경찰]입니다.', description="마피아를 찾아내고, 시민들을 구해 승리하세요.")
                        embed.set_image(url=Mafiaimage[2])
                        embed.add_field(name="소속", value="시민 팀", inline=False)
                    elif Job[i] == '의사':
                        embed = discord.Embed(title='당신의 직업은 [의사]입니다.', description="선량한 시민들을 지켜내고, 승리하세요.")
                        embed.set_image(url=Mafiaimage[3])
                        embed.add_field(name="소속", value="시민 팀", inline=False)
                    elif Job[i] == '시민':
                        embed = discord.Embed(title='당신의 직업은 [시민]입니다.', description="끝까지 살아남고, 미션을 수행하여 승리하세요.")
                        embed.set_image(url=Mafiaimage[4])
                        embed.add_field(name="소속", value="시민 팀", inline=False)
                    GameJob.append(f"{Player[i]}-{Job[i]}")
                    embed.set_footer(text="데마시아의 외교관", icon_url="https://media.discordapp.net/attachments/898797966666637354/964197572585590804/profile.jpg")
                    if author.dm_channel is None:
                        channel = await author.create_dm()    # 디엠 채널이 없으면 개설 후 메세지 전송 
                        await author.dm_channel.send(embed=embed)
                    elif author.dm_channel:                   # 있다면 바로 전송
                        await author.dm_channel.send(embed=embed)
                print(GameJob)
                await ctx.send(f"**::MAFIA:: 회색 도시의 밤 | 게임모드 :【{MafiaRule}】**")
                await asyncio.sleep(2)
                await ctx.send("==========================================")
                await ctx.send(f"[ {MafiaDate}일차 ] ☀️낮 (회의 시간 : 1분30초)")
                await ctx.send("==========================================")
                await asyncio.sleep(60)
                await ctx.send("회의 시간이 30초 남았습니다.")
                await asyncio.sleep(30)
                await ctx.send(f"<@&967000841309552640>") # 호출
                await ctx.send(f"회의 시간이 종료되었습니다. **지금부터 5초 이후 채팅을 치시면** 경고를 부여합니다.")
                await asyncio.sleep(5)
                if len(Player)%2 == 0:
                    half = len(Player)//2
                else:
                    half = len(Player)//2 + 1
                await ctx.send("==========================================")
                await ctx.send(f"🗳투표 시간이 시작됩니다. 마피아 용의자로 생각되는 사람을 투표해주세요.\n만약 원하신다면 본 투표에서 [기권표]를 행사하실 수 있으며, \n과반수({half}명)가 이를 선택한다면 이번 투표는 무효 처리 됩니다.\n투표시간은 30초입니다. `중복 투표 및 변경 절대 금지`")
                await ctx.send("==========================================")
                await asyncio.sleep(20)
                await ctx.send("10초 남았습니다.")
                await asyncio.sleep(5)
                await ctx.send("5초 남았습니다.")
                await asyncio.sleep(5)
                await ctx.send(f"<@&967000841309552640>") # 호출
                await ctx.send("투표 마감되었습니다.")
                await ctx.send("==========================================")
                await ctx.send(f"[ {MafiaDate}일차 ] 🌙밤 (진행 시간 : 1분30초)")
                await ctx.send("==========================================")
            elif MafiaRule == 'Royal':
                if len(Player) == 4:
                    Job = RoyalJob_4.copy()
                elif len(Player) == 5:
                    Job = RoyalJob_5.copy()
                elif len(Player) == 6:
                    Job = RoyalJob_6.copy()
                elif len(Player) == 7:
                    Job = RoyalJob_7.copy()
                elif len(Player) == 8:
                    Job = RoyalJob_8.copy()
                else:
                    await ctx.send("🚫[Royal] 인원 제한이 맞지 않아 게임이 시작되지 않았습니다. (최소 4인, 최대 8인)")
            elif MafiaRule == 'Royal_fanatic':
                if len(Player) == 9:
                    Job = RoyalJob_9.copy()
                else:
                    await ctx.send("🚫[Royal_fanatic] 인원 제한이 맞지 않아 게임이 시작되지 않았습니다. (9인)")
        else:
            await ctx.send("🚫게임이 이미 시작되었습니다. 다음 게임이 시작될 때까지 기다려주세요.")
    elif('설정' in message):
        if(message == '설정'):
            await ctx.send("아래 세가지 옵션 중 하나를 선택해주세요. (기본값 : Classic)")
            embed = discord.Embed(title="마피아 게임 설정", description="마피아 게임에 대한 설명이에요.\n 아래 명령어들을 통해 게임에 대한 설명과, 게임 진행이 가능합니다!", color=0x62c1cc) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
            embed.add_field(name="①:Classic", value="4~8인으로 구성되며, 직업이 마피아/경찰/의사/시민 으로만 구성되어있습니다.\n디스코드 내에 있는 보이스 채널등을 잘 활용하여, 승리하세요.", inline=False)
            embed.add_field(name="②:Royal", value="4~8인 직업 게임 `제작중입니다.`", inline=False)
            embed.add_field(name="③:Royal_fanatic", value="9인 전용 직업 게임 `제작중입니다.`", inline=False)
            embed.set_footer(text="데마시아의 외교관", icon_url="https://media.discordapp.net/attachments/898797966666637354/964197572585590804/profile.jpg")
            await ctx.send(embed=embed)
        else:
            SettingOfMafiaRule = message.split()
            if SettingOfMafiaRule[1] == '1':
                await ctx.send("게임 규칙이 Classic으로 설정되었습니다.")
                MafiaRule = MafiaRules[0]
            elif SettingOfMafiaRule[1] == '2':
                await ctx.send("게임 규칙 Royal은 현재 개발중입니다..")
                #MafiaRule = MafiaRules[1]
            elif SettingOfMafiaRule[1] == '3':
                await ctx.send("게임 규칙 Royal_fanatic은 현재 개발중입니다..")
                #MafiaRule = MafiaRules[2]
            else:
                await ctx.send("양식에 맞춰 재입력해주세요! =마피아 설정 (번호)")
    elif(message == '초기화'):
        MafiaGame = False
        Player = []
        NumberPlayer = []
        MafiaRule = 'Classic'
        await ctx.send("[System]개발단계 :: 마피아 시스템이 초기화 되었습니다.")