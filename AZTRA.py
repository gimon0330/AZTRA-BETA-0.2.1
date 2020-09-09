import discord,datetime,json,asyncio,urllib, urllib.request , bs4,requests,threading
from random import randint
from bs4 import BeautifulSoup
from discord.utils import get

start_time = datetime.datetime.utcnow()
client = discord.Client()
with open("./data/announcechannel.json", "r", encoding='UTF8') as db_json:  announcechannel = json.load(db_json)
with open("./data/serverprefix.json", "r", encoding='UTF8') as db_json:  serverprefix = json.load(db_json)
with open("./data/botblack.json", "r", encoding='UTF8') as db_json:  botblack = json.load(db_json)
with open("./data/hellochannel.json", "r", encoding='UTF8') as db_json:  hellochannel = json.load(db_json)
with open("./data/helloword.json", "r", encoding='UTF8') as db_json:  helloword = json.load(db_json)
with open("./data/byeword.json", "r", encoding='UTF8') as db_json:  byeword = json.load(db_json)
with open("./data/usercount.json", "r", encoding='UTF8') as db_json:  usercount = json.load(db_json)
with open("./data/enterrole.json", "r", encoding='UTF8') as db_json:  enterrole = json.load(db_json)
with open("./level/level.json", "r", encoding='UTF8') as db_json:  level = json.load(db_json)
with open("./config/config.json", "r", encoding='UTF8') as db_json:  botconfig = json.load(db_json)
with open("./config/errorlist.json", "r", encoding='UTF8') as db_json:  errorlist = json.load(db_json)
with open("./config/admindb.json", "r", encoding='UTF8') as db_json:  admindb = json.load(db_json)
botVersion = botconfig['VersionNum']
botVType = botconfig['VersionType']

admin = [467666650183761920,492645332908507137]
tester = []

presences_list = [f"AZTRA {botVType} V{botVersion}", "'+도움'으로 봇명령어 알아보기", str(len(client.guilds))+" Servers│"+str(len(client.users))+" Users"]

@client.event
async def bg_change_playing():
    while True:
        for v in presences_list:
            await asyncio.sleep(10)
            presences_list[2]=str(len(client.guilds))+"Servers│"+str(len(client.users))+" Users"
            await client.change_presence(activity=discord.Game(v))
        with open("./level/level.json", "w", encoding='UTF8') as db_json: db_json.write(json.dumps(level, ensure_ascii=False, indent=4))

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("Booting..."))
    client.loop.create_task(bg_change_playing())
    print("BOT ON") 

@client.event
async def on_member_join(member):
    guild=str(member.guild.id)
    if guild in hellochannel.keys():
        channel=client.get_channel(hellochannel[guild])
        say=helloword[guild].replace("(user)",member.name)
        say=say.replace("(mentionuser)",member.mention)
        await channel.send(say)
    if guild in usercount.keys():
        channel = client.get_channel(int(usercount[guild][0]))
        await channel.edit(name=usercount[guild][1].replace('[count]',str(len(member.guild.members))))

@client.event
async def on_member_remove(member):
    guild=str(member.guild.id)
    if guild in hellochannel.keys():
        channel=client.get_channel(hellochannel[guild])
        say=byeword[guild].replace("(user)",member.name)
        say=say.replace("(mentionuser)",member.mention)
        await channel.send(say)
    if guild in usercount.keys():
        channel = client.get_channel(int(usercount[guild][0]))
        await channel.edit(name=usercount[guild][1].replace('[count]',str(len(member.guild.members))))
            

def get_embed(title, description='', color=0xCCFFFF): return discord.Embed(title=title,description=description,color=color)

def slevel(guild,author):
    if guild not in level.keys(): level[guild] = {}
    if author not in level[guild].keys(): level[guild][author] = [0,0]
    level[guild][author][1] += 1
    if level[guild][author][1] >= level[guild][author][0] * 90 + 50:
        level[guild][author][1] = 0
        level[guild][author][0] = level[guild][author][0] + 1
    

@client.event
async def on_message(message): 
    if message.channel.type==discord.ChannelType.private:
        if message.content=='ㅎㅇ': await message.channel.send(embed=get_embed("ㅎㅇ", ""))
    else:
        if str(message.author.id) in botblack.keys(): return
        slevel(str(message.guild.id),str(message.author.id))
        if str(message.guild.id) in serverprefix.keys(): prefix=serverprefix[str(message.guild.id)] #서버별로 접두사 설정
        else: prefix='+'
        if message.content.startswith(prefix): msg = message.content[(len(prefix)):]
        else: return  
        if message.channel.permissions_for(message.guild.get_member(client.user.id)).send_messages:
            await message.author.send("메세지를 보낼 권한이 없습니다!!")
        try:
            if msg.startswith("접두사 변경"): #접두사 변경
                if len(msg.split(" ")) >= 4: assert False, 'ERROR CODE:0\n접두사는 띄어쓰기 없이 해주세요'
                if len(msg.split(" ")) == 2: assert False, f'ERROR CODE:1\n{prefix} 접두사 변경 (접두사)의 형식으로 사용해주세요'
                else: 
                    if str(message.guild.id) in serverprefix:
                        oldprefix = serverprefix[str(message.guild.id)]
                        serverprefix[str(message.guild.id)] = msg.split(" ")[2]
                        await message.channel.send(f"접두사를 {oldprefix}에서 {serverprefix[str(message.guild.id)]}로 변경했어요!")
                    else:
                        serverprefix[str(message.guild.id)] = msg.split(" ")[2]
                        await message.channel.send(f"접두사를 {serverprefix[str(message.guild.id)]}로 변경했어요!")
                    with open("./data/serverprefix.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(serverprefix, ensure_ascii=False, indent=4))
            elif msg.startswith("에러코드"): #에러코드
                try: code=int(msg.split(" ")[1])
                except ValueError: assert False, 'ERROR CODE:2\n코드 입력칸에는 정수형로 입력해주세요'
                except IndexError: assert False, f'ERROR CODE:3\n{prefix}에러코드 (코드 숫자)로 입력해주세요'
                if str(code) in errorlist.keys(): await message.channel.send(embed=get_embed(f"ERROR CODE : {code}",errorlist[str(code)].replace("[prefix]",prefix)))
                else: assert False, 'ERROR CODE:4\n없는 에러코드입니다.'
            elif msg=="공지채널 설정": #공지 채널 설정
                if message.channel.permissions_for(message.guild.get_member(client.user.id)).send_messages:
                    announcechannel[str(message.guild.id)] = message.channel.id
                    await message.channel.send(f"공지 채널을 {message.channel.name}로 변경했어요!")
                    with open("./data/announcechannel.json", "w", encoding='utf-8') as database_json:
                        database_json.write(json.dumps(announcechannel, ensure_ascii=False, indent=4))
                else: assert False, f"{message.channel.name}에 메세지를 보낼권한이 없습니다!"
            elif msg.startswith('공지보내'):
                if str(message.author.id) not in admindb.keys(): return
                lis =[]
                for s in client.guilds:
                    sendedserver = s.name
                    schannel = ''
                    if str(s.id) in announcechannel.keys():
                        schannel=client.get_channel(announcechannel[str(s.id)])
                    else:
                        for channel in s.text_channels:
                            if channel.permissions_for(s.get_member(client.user.id)).send_messages:
                                freechannel = channel
                                if '공지' in channel.name and '봇' in channel.name:
                                    schannel = channel
                                    break
                                elif 'noti' in channel.name.lower() and 'bot' in channel.name.lower():
                                    schannel = channel
                                    break
                                elif '공지' in channel.name:
                                    schannel = channel
                                    break
                                elif 'noti' in channel.name.lower():
                                    schannel = channel
                                    break
                                elif '봇' in channel.name:
                                    schannel = channel
                                    break
                                elif 'bot' in channel.name.lower():
                                    schannel = channel
                                    break
                        if schannel == '':
                            schannel = freechannel
                    try: 
                        await schannel.send(" ".join(msg.split(" ")[1:]))
                        lis.append('<a:689877466705297444:700213356078039061> '+sendedserver+' 성공')
                    except: 
                        lis.append('<a:689877428142604390:700213356564578315> '+sendedserver+' 실패')
                await message.channel.send(embed=get_embed("공지 전송 완료","\n".join(lis)))
            elif msg.startswith('프로필'):
                try: user = message.guild.get_member(int(message.mentions[0].id))
                except: user = message.author
                if user.display_name == user.name: embed = discord.Embed(title=user.name + " 님의 프로필", color=0xccffff)
                else: embed = discord.Embed(title=user.name + " 님의 프로필",description="닉네임 : (" + user.display_name + ")", color=0xccffff)
                embed.set_thumbnail(url=user.avatar_url)
                embed.add_field(name="유저 ID", value=str(user.id), inline=False)
                try:
                    st = str(user.status)
                    if st == "online": sta = ":green_circle: 온라인"
                    elif st == "offline": sta = ":black_circle: 오프라인"
                    elif st == "idle": sta = ":yellow_circle: 자리 비움"
                    else: sta = ":no_entry: 방해 금지"
                except: sta = "불러오는데 실패"
                embed.add_field(name="현재 상태", value=sta, inline=True)
                date = datetime.datetime.utcfromtimestamp(((int(message.author.id) >> 22) + 1420070400000)/1000)
                embed.add_field(name="Discord 가입 일시", value=str(date.year) + "년 " + str(date.month) + "월 " + str(date.day) + "일 ", inline=True)
                joat = user.joined_at.isoformat()
                embed.add_field(name="서버 가입 일시", value=joat[0:4]+'년 '+joat[5:7]+'월 '+joat[8:10]+'일', inline=True)
                if user.id in admin: embed.add_field(name="봇 권한", value="ADMIN", inline=True)
                elif user.id in tester: embed.add_field(name="봇 권한", value="BETA TESTER", inline=True)
                else : embed.add_field(name="봇 권한", value="USER", inline=True)
                if user.guild_permissions.administrator: embed.add_field(name="서버 권한", value="ADMIN", inline=True)
                else: embed.add_field(name="서버 권한", value="USER", inline=True)
                await message.channel.send(embed=embed)
            elif msg=='정보':
                embed = discord.Embed(title="**AZTRA**",description=f"AZTRA BOT Made By Aztra#0556\n> Made With Discord.py\n> Ver. {botVType} {botVersion}\n> Helpers. **다쿤#1914**\n**{len(client.guilds)}**SERVERS | **{len(client.users)}**USERS", color=0xCCffff)
                embed.set_footer(text="TEAM Infinite®️")
                embed.set_thumbnail(url=client.get_user(700122130246795344).avatar_url)
                await message.channel.send(embed=embed)
            elif msg=='서버정보':
                g=message.guild
                embed=discord.Embed(title=g.name,description=f'ID : {g.id}\n유저수 : **{len(g.members)}**명\n접두사 : {prefix}\n서버 개설자 : {g.owner.name}\n이모티콘 개수 : {len(g.roles)}',color=0xccffff)
                embed.set_thumbnail(url=message.guild.icon_url)
                await message.channel.send(embed=embed)
            elif msg.startswith('프사'):
                try: author = message.guild.get_member(int(message.mentions[0].id))
                except: author = message.author
                await message.channel.send(embed=get_embed(f"{author.name}님의 프로필사진","").set_image(url=author.avatar_url))
            elif msg.startswith('찬반투표'):
                smsg=await message.channel.send(embed=get_embed(f'{" ".join(message.content.split(" ")[1:])}',f"By. {message.author.display_name}"))
                await smsg.add_reaction('<a:689877466705297444:700213356078039061>')
                await smsg.add_reaction('<a:689877428142604390:700213356564578315>')
            elif msg.startswith('청소'):
                if message.author.guild_permissions.manage_messages == True:    
                    if message.guild.get_member(client.user.id).guild_permissions.manage_messages == True:    
                        try: lim=int(message.content.split(" ")[1])
                        except: assert False, f"ERROR CODE:8\n{prefix}청소 (갯수)로 입력해주세요."
                        try: await message.channel.purge(limit=lim)
                        except: assert False, f"ERROR CODE:10\n봇에게 채팅관리 권한이 없습니다"
                        dmsg = await message.channel.send(f"{lim}개의 메세지를 삭제 하였습니다")
                        await asyncio.sleep(3)
                        await dmsg.delete()
                    else: assert False, 'ERROR CODE:124\n봇에게 메세지를 지울 권한이 없습니다.'
                else: assert False, 'ERROR CODE:9\n채팅 관리 권한이 있어야 사용가능한 명령어 입니다.'
            elif msg=='서버 사진':
                embed=get_embed(f"{message.guild.name} 서버의 서버 사진","")
                embed.set_image(url=message.guild.icon_url)
                await message.channel.send(embed=embed)
            elif msg=='한강':
                await message.channel.send(embed=get_embed(':droplet: '+BeautifulSoup(requests.get('https://www.wpws.kr/hangang/').text, 'html.parser').select('#temp')[0].text,""))
            elif msg.startswith("업타임"):
                delta = datetime.datetime.utcnow() - start_time
                hours, remainder = divmod(int(delta.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                days, hours = divmod(hours, 24)
                if days: time_format = f"**{days}**일, **{hours}**시간, **{minutes}**분, and **{seconds}**초"
                else: time_format = f"**{hours}**시간, **{minutes}**분, **{seconds}**초"
                await message.channel.send(f"{time_format} 동안 깨어 있었어요!")
            elif msg.startswith("블랙추가"):
                if str(message.author.id) not in admindb.keys(): return
                user=str(msg.split(" ")[1])
                botblack[user]="blacklist"
                with open("./data/botblack.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(botblack, ensure_ascii=False, indent=4))
            elif msg.startswith("블랙제거"):
                if str(message.author.id) not in admindb.keys(): return
                user=str(msg.split(" ")[1])
                del botblack[user]
                with open("./data/botblack.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(botblack, ensure_ascii=False, indent=4))
            elif msg.startswith("eval"):
                if message.author.id != 467666650183761920: return
                com = " ".join(message.content.split(" ")[1:])
                try:await message.channel.send(embed=discord.Embed(title='관리자 기능 - Eval',description=f"📤 OUTPUT```{eval(com)}```",color=0xCCFFFF))
                except Exception as evalex:await message.channel.send(embed=discord.Embed(title='관리자 기능 - Eval',description=f"📤 EXCEPT```{evalex}```",color=0xFF0000))
            elif msg.startswith("await"):
                if message.author.id != 467666650183761920: return
                command = " ".join(message.content.split(" ")[1:])
                try: await eval(command)
                except Exception as evalex: await message.channel.send(embed=discord.Embed(title='관리자 기능 - Eval',description=f"📤 EXCEPT```{evalex}```",color=0xFF0000))
            elif msg.startswith("exec"):
                if message.author.id != 467666650183761920: return
                command = " ".join(message.content.split(" ")[1:])
                try: arg = exec(command)
                except Exception as evalex: await message.channel.send(embed=discord.Embed(title='관리자 기능 - EXEC',description=f"📤 EXCEPT```{evalex}```",color=0xFF0000))
            elif msg=='도움' or msg=='명령어':
                embed=discord.Embed(title="**AZTRA** 명령어",description=f"<>괄호는 필수 []괄호는 비워도 됩니다\n현재 서버의 접두사는 {prefix}입니다. 명령어 앞에 접두사를 붙여주세요",color=0xccffff)
                embed.add_field(name='정보',value='```프로필 [@멘션], 정보, 서버정보, 프사 [@멘션], 서버사진, 디엠 공지 <할말>```',inline=False)
                embed.add_field(name='관리',value='```청소 <갯수>, 찬반투표 <할말>, 킥 <@멘션>, 밴 <@맨션>, 인삿말 도움```',inline=False)
                embed.add_field(name='봇관련',value='```접두사 변경 <접두사>, 에러코드 <코드>, 공지채널 설정, 업타임```',inline=False)
                embed.add_field(name='기타',value='```한강```',inline=False)
                await message.channel.send(embed=embed)
            elif msg=='핑':
                ping = round(1000 * client.latency,3)
                if ping <= 100: pinglevel = '🔵 매우좋음'
                elif ping <= 250: pinglevel = '🟢 양호함'
                elif ping <= 400: pinglevel = '🟡 보통'
                elif ping <= 550: pinglevel = '🔴 나쁨'
                elif ping > 550: pinglevel = '⚫ 매우나쁨'
                await message.channel.send(embed=get_embed('🏓 퐁!',f'**디스코드 지연시간: **{ping}ms - {pinglevel}'))
            elif msg.startswith("서버"):
                servers = []
                for s in client.guilds: servers.append([s.name, len(s.members), s.owner.name])
                servers.sort(key=lambda x:x[1], reverse=True)
                embed=discord.Embed(title="**AZTRA SERVER**",description=f'총 {len(client.guilds)}개의 서버, {len(client.users)}명의 유저와 함께 하는중', color=0xCCFFFF)
                try: n=(int(message.content.split(" ")[1])-1)*10
                except IndexError: n = 0
                except ValueError: assert False, 'ERROR CODE:4\n값에는 숫자만 입력해주세요'
                for x in range(n,n+10):
                    if x == 0: s = ':first_place:'
                    elif x == 1: s = ':second_place:'
                    elif x == 2: s = ':third_place:'
                    elif x <= 9: s = ':medal:'
                    else: s=''
                    try: embed.add_field(name=s+' '+str(x+1)+'위 '+str(servers[x][0]), value="인원 : " + str(servers[x][1]) + ", 서버 주인 : " + str(servers[x][2]), inline=False)
                    except: break
                await message.channel.send(embed=embed)
            elif msg.startswith("밴"):
                if message.author.guild_permissions.ban_members:
                    try: user=client.get_user(int(message.mentions[0].id))
                    except IndexError: 
                        await message.channel.send("!킥 @멘션 으로 사용해주세요.")
                        return
                    await message.guild.ban(user,reason=f'banned by {message.author.name}', delete_message_days=3)
                    await message.channel.send("밴 완료!")
                else: await message.channel.send("유저 차단하기 권한이 없어서 불가능합니다.")
            elif msg.startswith("킥"):
                if message.author.guild_permissions.kick_members:
                    try: user=client.get_user(int(message.mentions[0].id))
                    except IndexError: 
                        await message.channel.send("!킥 @멘션 으로 사용해주세요.")
                        return
                    await message.guild.kick(user)
                    await message.channel.send("킥 완료!")
                else: await message.channel.send("유저 추방 하기 권한이 없어서 불가능합니다.")
            elif msg.startswith("디엠 공지"):
                if message.author != message.guild.owner: assert False, "소버 소유자만 가능합니다"
                smsg=" ".join(msg.split(" ")[2:])
                if smsg == "": assert False,'ERROR CODE:10\n디엠 공지 (디엠으로 보낼말) 을 적어주세요'
                sendeduser=[]
                for s in message.guild.members:
                    if s.bot == False:
                        try:
                            await s.send(smsg)
                            sendeduser.append(f'<a:689877466705297444:700213356078039061>> **{s.name}**님에게 전송 성공')
                        except: sendeduser.append(f'<a:689877428142604390:700213356564578315>> **{s.name}**님에게 전송 실패')
                await message.channel.send(embed=get_embed("공지 전송 로그","\n".join(sendeduser)))
            elif msg=='인사 채널 설정':
                if message.author != message.guild.owner: assert False, "소버 소유자만 가능합니다"
                hellochannel[str(message.guild.id)]=message.channel.id
                helloword[str(message.guild.id)]='(mentionuser)님 안녕하세요'
                byeword[str(message.guild.id)]='(user)님 안녕히가세요'
                await message.channel.send(f"{message.channel.name}으로 인삿말을 보내겠습니다\n<{prefix}입장공지>, <{prefix}퇴장공지>으로 인사 문구를 설정해주세요\n<{prefix}인삿말 도움>으로 도움말을 보세요!")
                with open("./data/hellochannel.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(hellochannel, ensure_ascii=False, indent=4))
                with open("./data/helloword.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(helloword, ensure_ascii=False, indent=4))
                with open("./data/byeword.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(byeword, ensure_ascii=False, indent=4))
            elif msg.startswith("입장공지"):
                if message.author != message.guild.owner: assert False, "소버 소유자만 가능합니다"
                if str(message.guild.id) in hellochannel.keys():
                    word=" ".join(msg.split(" ")[1:])
                    assert word=='','ErrorCode:11\n'
                    helloword[str(message.guild.id)]=word
                    await message.channel.send(f'누군가 들어오면\n{helloword[str(message.guild.id)]}\n라고 하겠습니다.')
                    with open("./data/helloword.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(helloword, ensure_ascii=False, indent=4))
                else: await message.channel.send(f"<{prefix}인사 채널 설정> 으로 채널 설정 먼저 하고 오세요")
            elif msg.startswith("퇴장공지"):
                if message.author != message.guild.owner: assert False, "소버 소유자만 가능합니다"
                if str(message.guild.id) in hellochannel.keys():
                    word=" ".join(msg.split(" ")[1:])
                    assert word=='','ErrorCode:11\n'
                    byeword[str(message.guild.id)]=word
                    await message.channel.send(f'누군가 들어오면\n{byeword[str(message.guild.id)]}\n라고 하겠습니다.')
                    with open("./data/byeword.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(byeword, ensure_ascii=False, indent=4))
                else: await message.channel.send(f"<{prefix}인사 채널 설정> 으로 채널 설정 먼저 하고 오세요")
            elif msg=='인삿말 도움':
                embed=get_embed("인삿말 명령어","")
                embed.add_field(name=f'{prefix}인사 채널 설정',value='```메세지를 적은 채널에 봇이 다른 유저가 입장할시 인사를 해줍니다```',inline=False)
                embed.add_field(name=f'{prefix}입장공지 (할말), {prefix}퇴장공지 (할말)',value='```입장 채널을 설정한곳에 보낼 문구를 정합니다\n도중에 (user)이라고 하면, 봇이 들어온 유저의 이름을 바꿔적고\n(mentionuser)이라고 하면 해당위치에 유저를 맨션합니다.\nex) (user)님 안녕하세요\n--> TH_PHEC님 안녕하세요 로 바뀝니다```',inline=False)
                await message.channel.send(embed=embed)
            elif msg.startswith("인원채널추가"):
                if message.author.guild_permissions.administrator == False: assert False, "서버 관리자만 가능합니다"
                if str(message.guild.id) in usercount.keys(): assert False, f'이미 채널이 있습니다! {prefix}인원채널삭제를 이용해서 삭제후 다시 해주세요'
                word=" ".join(msg.split(" ")[1:])
                if word == '': assert False, f"{prefix}인원채널추가 (채널이름) 으로 사용해주세요.\n[count]를 중간에 넣으시면 그위치에 인원 숫자가 표시됩니다" #비었을때 에러
                if "[count]" not in word: assert False, f'[count]를 중간에 넣으시면 그위치에 인원 숫자가 표시됩니다' #[count]가 없을때 에러
                cha = await message.guild.create_voice_channel(word.replace('[count]',str(len(message.guild.members))))
                await cha.set_permissions(message.guild.default_role, connect=False)
                usercount[str(message.guild.id)]=[cha.id,word]
                await message.channel.send(f"{usercount[str(message.guild.id)][1].replace('[count]',str(len(message.guild.members)))} 의 형식 으로 표시됩니다\n채널을 삭제할때 {prefix}인원채널삭제 를 사용해서 삭제해주세요")
                with open("./data/usercount.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(usercount, ensure_ascii=False, indent=4))
            elif msg=='인원채널삭제':
                if message.author.guild_permissions.administrator == False: assert False, "서버 관리자만 가능합니다"
                if str(message.guild.id) not in usercount.keys(): assert False, '삭제할 채널이 없습니다!'
                channel = client.get_channel(usercount[str(message.guild.id)][0])
                try: await channel.delete(reason=f"Erased By {message.author.name}")
                except : pass
                del usercount[str(message.guild.id)]
                await message.channel.send("채널이 삭제되었습니다.")
                with open("./data/usercount.json", "w", encoding='utf-8') as database_json: database_json.write(json.dumps(usercount, ensure_ascii=False, indent=4))
            elif msg=='레벨':
                await message.channel.send(f"{message.author.name}님의 현재 레벨은 **{level[str(message.guild.id)][str(message.author.id)][0]}**, 경험치는 **{level[str(message.guild.id)][str(message.author.id)][1]}** 입니다")
            elif msg=='초대장':
                await message.channel.send("https://discordapp.com/api/oauth2/authorize?client_id=700122130246795344&permissions=8&scope=bot")
            elif msg.startswith("숫자뽑기"):
                try: a=int(msg.split(" ")[1])
                except IndexError: assert False, f'{prefix}숫자뽑기 (시작숫자) (끝숫자)의 형식으로 사용해주세요'
                except TypeError: assert False, f'값을 입력하는 칸에는 숫자만 넣어주세요'
                try: b=int(msg.split(" ")[2])
                except TypeError: assert False, f'값을 입력하는 칸에는 숫자만 넣어주세요'
                except IndexError: assert False, f'{prefix}숫자뽑기 (시작숫자) (끝숫자)의 형식으로 사용해주세요'
                await message.channel.send(randint(a,b))
            elif msg.startswith("뽑기"):
                s=msg.split(" ")[1:]
                if len(s) == 0: assert False, f'{prefix}뽑기 (항목) (항목)의 형식으로 사용해주세요\n아무런 값도 입력받지 못했어요!'
                if len(s) == 1: assert False, f'{prefix}뽑기 (항목) (항목)의 형식으로 사용해주세요\n값이 한개면 뽑을 이유는 없잖아요!'
                await message.channel.send(s[randint(0,len(s)-1)])
            elif msg.startswith("계산"):
                command =str(" ".join(msg.split(" ")[1:]))
                command=command.replace("^","**")
                try: res = int(eval(command))
                except: assert False, '숫자의 단순 연산만 가능합니다'
                if len(str(res)) >= 2000: assert False, '계산 결과가 너무 큽니다!'
                embed=get_embed("계산결과",'')
                embed.add_field(name='📥 INPUT',value=f"```{command}```",inline=False)
                embed.add_field(name='📤 OUTPUT',value=f"```{res}```",inline=False)
                await message.channel.send(embed=embed)
            elif msg=='사람뽑아':
                lis = []
                for s in message.guild.members:
                    if s.bot == False:
                        lis.append(s.name)
                await message.channel.send(lis[randint(0,len(lis))])
            elif msg.startswith("역할돌려"):
                if message.guild.get_member(700122130246795344).Permissions.manage_roles == False: assert False, 'ERROR CODE:39\n봇에게 역할관리 권한이 없습니다.'
                try: roleid = int(msg.split(" ")[1])
                except ValueError: assert False, 'ERROR CODE:40\n{prefix}역할돌려 (역할아이디)로 사용해주세요\n역할아이디에는 숫자만 넣어주세요'
                except IndexError: assert False, 'ERROR CODE:41\n{prefix}역할돌려 (역할아이디)로 사용해주세요'
                role = message.guild.get_role(roleid)
                sendeduser=[]
                for member in message.guild.members:
                    if member.bot == False:
                        if role in member.roles:
                            sendeduser.append(f'> <a:689877428142604390:700213356564578315> **{member.name}** 실패')
                        else:
                            sendeduser.append(f'> <a:689877466705297444:700213356078039061> **{member.name}** 성공')
                            await discord.Member.add_roles(member, role)
                await message.channel.send(embed=get_embed("역할 로그","\n".join(sendeduser)))
            elif msg=='주사위':
                randomNum = randint(1,6)
                if randomNum == 1: num = ':one:'
                elif randomNum==2: num = ':two:'
                elif randomNum==3: num = ':three:'
                elif randomNum==4: num = ':four:'
                elif randomNum==5: num = ':five:'
                elif randomNum==6: num = ':six:'
                await message.channel.send(embed=discord.Embed(description=num))
            elif msg=='빌보드':
                delmsg=await message.channel.send("불러오는 중입니다 잠시만 기다려 주세요...")
                soup = BeautifulSoup(requests.get('https://www.billboard.com/charts/hot-100').text, 'html.parser')
                embed = discord.Embed(title='BillBoard TOP 10',color=0xCCFFFF)
                for a in range(1,11):
                    title=soup.select(f"#charts > div > div.chart-list.container > ol > li:nth-child({a}) > button > span.chart-element__information > span.chart-element__information__song.text--truncate.color--primary")[0].text
                    author=soup.select(f"#charts > div > div.chart-list.container > ol > li:nth-child({a}) > button > span.chart-element__information > span.chart-element__information__artist.text--truncate.color--secondary")[0].text
                    embed.add_field(name=f'Top{a} {title}',value=f'{author}',inline=False)
                await delmsg.delete()
                await message.channel.send(embed=embed)
            elif msg=='초대장':
                await message.channel.send(f"https://discordapp.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot")
            elif msg=='서포트서버':
                await message.channel.send("https://discord.gg/vdcurrQ")

        except Exception as ex: 
            if message.channel.permissions_for(message.guild.me).send_messages == False:
                await message.author.send(embed=get_embed("ERROR!",f"```봇이 채팅방에 메세지를 보내지 못합니다!```\n",0xFF0000))
            else:
                if ex == AssertionError: await message.channel.send(embed=get_embed("ERROR!",f"```{ex}```\n**{prefix}에러코드 (CODE) 로 도움말을 보실수 있습니다.",0xFF0000))
                else: await message.channel.send(embed=get_embed("ERROR!",f"```{ex}```\n**\📞 '{prefix}서포트서버'로 서포트서버에 오실수 있습니다.",0xFF0000))

client.run(botconfig["token"])