import os
import json
import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']

client = commands.Bot(command_prefix='$')


URL ="https://remedious-api.herokuapp.com/"
request = requests.get(URL + "dashboard",headers={
"email":"email4",
"password":"123"
})

json_response = request.json()
symptons_list = json_response['Symptoms Details']
remedy_list = json_response['Remedy Details']
@client.command()
async def FAQ(ctx):
    embedVar = discord.Embed(title="Commonly Asked Questions", description="called by "+ctx.author.mention, color=0x115ad1)
    embedVar.add_field(name="What is Remedious?", value="Remedious is a platform where you can get information about treatments and remedies for common symptoms related to COVID-19", inline=False)
    embedVar.add_field(name="What is ‘Long Covid’?", value ="Long Covid describes a set of symptoms that continue long after the initial Covid-19 infection has gone. Even people who had relatively moderate Covid-19 at the time can experience long covid symptoms. So can young, fit people.", inline=False)
    embedVar.add_field(name="What are the effects of Long Covid?", value="You don't have to be admitted to hospital with Covid-19 to have Long Covid but one British Medical Journal paper looked at what happened to those who were admitted (about 450,000 of them) after they were discharged. All told, one third of discharged patients were readmitted to hospital and one in 10 died.", inline=False)
    embedVar.add_field(name="What are some symptoms of Long Covid?", value="Run `$symptoms` to see a full list", inline=False)
    embedVar.add_field(name="What are some remedies I can follow?", value="Run `$remedies` to see a full list", inline=False)
    await ctx.send(embed = embedVar)

@client.command()
async def symptoms(ctx):
    embedVar = discord.Embed(title="Symptoms on Remedious",description="called by "+ctx.author.mention, color=0x115ad1)
    for i in range(len(symptons_list)):
        embedVar.add_field(name=symptons_list[i]['symptoms'], value="level = "+symptons_list[i]['level'], inline=False)
    await ctx.send(embed=embedVar)

@client.command()
async def remedies(ctx):
    embedVar = discord.Embed(title="Remedies on Remedious",description="called by "+ctx.author.mention, color=0x115ad1)
    for i in range(len(remedy_list)):
        embedVar.add_field(name=remedy_list[i]['name'], value="level = "+ remedy_list[i]['level'],inline=False)
    await ctx.send(embed=embedVar)

@client.command()
async def remedy(ctx,*,rem):
    for i in range(len(remedy_list)):
        if remedy_list[i]['name']==rem:
            index = i
            break
    try:
        remedy = remedy_list[index]
        embedVar = discord.Embed(title=rem,description="called by "+ctx.author.mention, color=0x115ad1)
        embedVar.add_field(name = "Name",value=rem)
        embedVar.add_field(name = "Frequency", value=remedy['frequency'])
        embedVar.add_field(name = "Level", value=remedy['level'])
        embedVar.add_field(name = "Amount", value=remedy['amount'])
        embedVar.add_field(name = "Symptom Frequency", value=remedy['symptom_frequency'])

    except:
        await ctx.send("Invalid remedy")
        return
    await ctx.send(embed=embedVar)

@client.command()
async def sympton(ctx,*,symp):
    for i in range(len(symptons_list)):
        if symptons_list[i]['symptoms']==symp:
            index = i
            break
    try:
        symp_data = symptons_list[index]
        embedVar = discord.Embed(title=symp,description="called by "+ctx.author.mention, color=0x115ad1)
        embedVar.add_field(name = "Name",value=symp)
        embedVar.add_field(name = "Frequency", value=symp_data['frequency'])
        embedVar.add_field(name = "Level", value=symp_data['level'])  
    except:
        await ctx.send("Invalid sympton")
        return
    await ctx.send(embed=embedVar)

client.run(TOKEN)
