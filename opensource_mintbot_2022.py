import discord
from discord import app_commands, ButtonStyle, Object
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from discord.ui import Button, View
from datetime import datetime
from pprint import pprint
from gpiozero import CPUTemperature
import os
import random
import psutil, pytz, requests, cpuinfo
import urllib.request
import platform


# Maintainer mint3100 (Github)
# if you update Mintbot's version. you should change "version", "update_date" value.

year = datetime.today().year
today = datetime.today().now()
token = "YOUR TOKEN"


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all())
        self.synced = False #두번 동기화 안되게 방지

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #빗금 명령어가 동기화 되었는지 확인
            await tree.sync()
            self.synced = True
        print("--------------------------")
        print(f"{self.user}로 로그인 되었습니다..!")
        print("--------------------------")
        print("Made with Heart in Mint")
        await client.change_presence(status=discord.Status.online, activity=discord.Game(""))


client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(name = '시간', description='현재 시간은?')
async def date(interaction: discord.Interaction):
    embed = discord.Embed(title = ':calendar: 현재 날짜/시간', description = str(datetime.today().strftime("%Y년 %m월 %d일 %H시 %M분")) + " 입니다!", color = 0x62c1cc) # 기능
    embed.set_author(name="MintBOT", icon_url="") #이미지
    await interaction.response.send_message(embed=embed)

@tree.command(name = '핑', description='너와 나의 핑 차이 (?)')
async def ping(interaction: discord.Interaction):
    embed = discord.Embed(title = ':ping_pong: 퐁!', description = str(round(client.latency * 1000)) + 'ms', color = 0x62c1cc) #기능
    embed.set_author(name="MintBOT", icon_url="") #이미지
    await interaction.response.send_message(embed=embed)


@tree.command(name = '주사위', description='주사위 굴리기')  
async def dice(interaction: discord.Interaction):
    dice = "주사위 숫자 1이 나왔습니다!", "주사위 숫자 2가 나왔습니다!", "주사위 숫자 3이 나왔습니다!", "주사위 숫자 4가 나왔습니다!", "주사위 숫자 5가 나왔습니다!", "주사위 숫자 6이 나왔습니다!"
    embed = discord.Embed(title = random.choice(dice), color = 0x62c1cc)
    embed.set_author(name="MintBOT", icon_url="")
    await interaction.response.send_message(embed=embed)


@tree.command(name = '서버', description='서버 상황을 알려드려요..!')
async def info(interaction: discord.Interaction):
    cpu = cpuinfo.get_cpu_info()
    embed = discord.Embed(title="서버 사용량", color=0x62c1cc)
    embed.set_author(name="MintBOT", icon_url="")
    embed.add_field(name="CPU이름", value=cpu['brand_raw'], inline=True)
    embed.add_field(name="사용중인 램", value=str(round((psutil.virtual_memory().used) * 0.00000000093132, 1))+"GB", inline=True)
    embed.add_field(name="남은램", value=str(round(psutil.virtual_memory().free * 0.00000000093132, 1))+"GB", inline=True)
    embed.add_field(name="전체 램", value=str(round(psutil.virtual_memory().total * 0.00000000093132, 1))+"GB", inline=True)
    embed.add_field(name = 'CPU 사용량', value = str(psutil.cpu_percent()) + '%', inline=True)
    await interaction.response.send_message(embed=embed)

@tree.command(name = "번역기", description = "번역기를 샤용해보세요..!",)
async def papago(interaction: discord.Interaction, 원문: str, 원어: str, 번역어: str):
    lan = 원어
    so = 번역어
    text2 = 원문
    if so.isupper() == True:
        print("검출")
        so = so.lower()
        papago()
    else:
        if 원어 == "언어감지":
            # language detect
            client_id = "YOUR CLIENT ID"
            client_secret = "YOUR CLIENT SECRET"
            data = "query=" + text2
            url = "https://openapi.naver.com/v1/papago/detectLangs"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            response_body = response.read()
            res = response_body.decode('utf-8')
            res1 = str(res)
            res2 = res1.split('"')
            res3 = res2[3]

            button1 = Button(label="네", style=ButtonStyle.primary)
            button2 = Button(label="아니요", style=ButtonStyle.primary)

            # Button 1 ("yes" Button) interaction.
            async def button1_callback(interaction: discord.Interaction):
                lan = res2[3]
                client_id = "YOUR CLIENT ID"
                client_secret = "YOUR CLIENT SECRET"
                data = {'text' : text2,'source' : lan,'target': so}
                header = {"X-Naver-Client-Id":client_id, "X-Naver-Client-Secret":client_secret}
                url = "https://openapi.naver.com/v1/papago/n2mt"
                response = requests.post(url, headers=header, data= data)
                rescode = response.status_code
                t_data = response.json()

                # embed parts
                embed = discord.Embed(title="번역기", description = "번역을 해드려요..!", color=0x62c1cc)
                embed.add_field(name="원문", value="```" + 원문 + "```", inline=False)
                embed.add_field(name="번역문", value="```" + t_data['message']['result']['translatedText'] + "```", inline=False)
                embed.add_field(name="원본 언어", value=res3 + " [언어감지]", inline=True)
                embed.add_field(name="번역 언어", value=so, inline=True)
                embed.set_author(name="MintBOT", icon_url="") 
                await interaction.response.send_message(embed=embed)

            # Button UI   
            async def button2_callback(interaction: discord.Interaction):
                await interaction.response.send_message("수동번역을 시도해주세요..!")

            button1.callback = button1_callback
            button2.callback = button2_callback
            view = View()
            view.add_item(button1)
            view.add_item(button2)
            await interaction.response.send_message(res3 + ' 이(가) 맞나요?', view=view, ephemeral = True)
        else:
        
            # 번역 시작
            client_id = "YOUR CLIENT ID"
            client_secret = "YOUR CLIENT SECRET"
            data = {'text' : text2,'source' : lan,'target': so}
            header = {"X-Naver-Client-Id":client_id, "X-Naver-Client-Secret":client_secret}
            url = "https://openapi.naver.com/v1/papago/n2mt"
            response = requests.post(url, headers=header, data= data)
            rescode = response.status_code
            t_data = response.json()
            
            embed = discord.Embed(title="번역기", description = "번역을 해드려요..!", color=0x62c1cc)
            embed.add_field(name="원문", value="```" + 원문 + "```", inline=False)
            embed.add_field(name="번역문", value="```" + t_data['message']['result']['translatedText'] + "```", inline=False)
            embed.add_field(name="원본 언어", value=lan + " [언어감지]", inline=True)
            embed.add_field(name="번역 언어", value=so, inline=True)
            embed.set_author(name="MintBOT", icon_url="") 
            await interaction.response.send_message(embed=embed)


# <-------- END ------->

#ClientKEY
client.run(token)