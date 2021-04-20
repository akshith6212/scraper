import discord
import requests
from requests_html import HTML,AsyncHTMLSession
from bs4 import BeautifulSoup as bs
from github import Github
from datetime import datetime

session = AsyncHTMLSession()
client = discord.Client()
html = open('template.html')
soup = bs(html,'html.parser')
confirmlink = 0
link = ''

async def scraper(link):
    print(link,'this is the link')
    r = await session.get(link)
    await r.html.arender()

    contest_ranks = r.html.find('#contest_rank')[0]

    solved_questions = []
    users = []

    members = contest_ranks.find('.solved')
    cnt = 0

    for member in members:
        solved_questions.append(member.text)
        user = member.find('a')[0].attrs['href']
        user = user.split('/')[1]
        users.append(user)
        # print(user,member.text)
        cnt += 1
        if cnt == 5:
            break
            
    title_html = r.html.find('title')[0]
    s = ''
    s = title_html.text
    s = s.split()
    
    title = ''
    for temp in s:
        if temp == '-':
            break
        title += temp
        title += ' '

    return users,solved_questions,title
    
async def func(users,solved,title):
    title_ = "<h1><svg class=\"ico-cup\"><use xlink:href=\"#cup\"></use></svg>"
    title_ += title
    title_ += '</h1>'
    title_html = soup.find('h1')
    title_html.replace_with(bs(title_, 'html.parser'))
    print(title_html)
      
    cnt = 0
    for req in soup.find_all('mark'):
        req.string = users[cnt]
        cnt += 1

    cnt = 0
    for req in soup.find_all('small'):
        req.string = solved[cnt]
        cnt += 1
      
    with open("final.html", "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))
        f_output.close()

    f_html = open('final.html')
    f = f_html.readlines()

    with open('leaderboard.html','r') as file:
        data = file.readlines()

    databefore = data[:404]
    dataafter = data[404:]

    data = databefore
    data += f
    data += dataafter

    with open('leaderboard.html','w') as file:
        file.writelines(data)

    # print(title_html)
    
async def push_git():
    # using an access token
    g = Github("TOKEN")

    f = open('leaderboard.html')
    content = f.read()   
    
    repo = g.get_repo("CPHub-NITC/test_akshith")
    contents = repo.get_contents("leaderboard.html")
    # print(contents)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    msg = "Auto Commit Scraper bot " + current_time
    repo.update_file(contents.path,msg, content,contents.sha, branch="main")


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$help'):
        s1 = '```'
        s2 = '$start \'link\' for starting the scraping \n'
        sl = 'eg: $start https://vjudge.net/contest/421836#rank \n\n'
        s3 = '$help for this'
        s4 = '$push for pushing into the github repo \n'
        help_msg = s1+s2+sl+s4+s3+s1
        await message.channel.send(help_msg)
        
    if message.content.startswith('$push'):
        push_git()


    if message.content.startswith('$yl'):
        confirmlink = 1
        global link
        if link != '':
            try:
                await message.channel.send('started scraping')
                await scraper(link)
                users,solved,title = await scraper(link)
                print(users)
                print(solved)
                print(title)
                await func(users,solved,title)
                await message.channel.send('done scraping time to push to git \n $push for pushing into the repo :) ')
                link = ''
            except:
                await message.channel.send('send a valid link again')
        else:
            await message.channel.send('try sending link again')

    if message.content.startswith('$nl'):
        # global link
        link = ''
        await message.channel.send('Discarded')

    if message.content.startswith('$start'):
        msg = message.content
        print(msg)
        messages = msg.split(' ')
        # global link
        link = ''
        try:
            link = messages[1]
        except:
            await message.channel.send('Please send a link')

        if link != '':
            print('link is not empty')
            print(link)

            try:
                response = requests.get(link)
                if '#rank' not in link:
                    link += '#rank'
                await message.channel.send('please confirm the link: ')
                await message.channel.send(link)
                await message.channel.send('(yl/nl)')
            except:
                await message.channel.send('Give a valid link')

 
client.run('TOKEN')

