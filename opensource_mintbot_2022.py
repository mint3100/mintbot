import discord
from discord import app_commands
from datetime import datetime
import random

# Project MintBot OpenSource (2020 ~ 2023)
# Last Maintainer : mint3100 (Github), End of Service
# Created : 2020.04.12
# Last Modified : 2024.05.29
# Version : 4.0.0 (Major Update 4)

token = "봇 토큰을 넣어주세요."


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all())
        self.synced = False #두번 동기화 안되게 방지

    async def on_ready(self):
        global botname
        # 봇 이름은 Discord 개발자 포털에 등록된 봇 이름입니다.
        botname = str(client.user).split("#")[0]
        await self.wait_until_ready()
        if not self.synced: #빗금 명령어가 동기화 되었는지 확인
            await tree.sync()
            self.synced = True
        print("--------------------------")
        print(f"{self.user}로 로그인 되었습니다..!")
        print("--------------------------")
        print("Project Url : https://github.com/mint3100/mintbot")
        await client.change_presence(status=discord.Status.online, activity=discord.Game(""))


client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(name = '시간', description='현재 시간은?')
async def date(interaction: discord.Interaction):
    embed = discord.Embed(title = ':calendar: 현재 날짜/시간', description = str(datetime.today().strftime("%Y년 %m월 %d일 %H시 %M분")) + " 입니다!", color = 0x62c1cc) # 기능
    embed.set_author(name=botname, icon_url="") #이미지
    await interaction.response.send_message(embed=embed)

@tree.command(name = '핑', description='너와 나 사이의 핑 차이')
async def ping(interaction: discord.Interaction):
    embed = discord.Embed(title = ':ping_pong: 퐁!', description = str(round(client.latency * 1000)) + 'ms', color = 0x62c1cc) #기능
    embed.set_author(name=botname, icon_url="") #이미지
    await interaction.response.send_message(embed=embed)


@tree.command(name = '주사위', description='주사위 굴리기')  
async def dice(interaction: discord.Interaction):
    dice = "주사위 숫자 1이 나왔습니다!", "주사위 숫자 2가 나왔습니다!", "주사위 숫자 3이 나왔습니다!", "주사위 숫자 4가 나왔습니다!", "주사위 숫자 5가 나왔습니다!", "주사위 숫자 6이 나왔습니다!"
    embed = discord.Embed(title = random.choice(dice), color = 0x62c1cc)
    embed.set_author(name=botname, icon_url="")
    await interaction.response.send_message(embed=embed)

@tree.command(name = 'test', description="테스트 메시지입니다. 이 부분을 복사해서 응답을 생성하세요.")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("본 메시지는 테스트 메시지입니다.")

# <-------- END ------->

#ClientKEY
client.run(token)